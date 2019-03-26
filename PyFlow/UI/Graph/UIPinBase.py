"""@file Pin.py
"""
import weakref

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QInputDialog

from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Graph.Painters import PinPainter


UI_PINS_FACTORIES = {}


class UICommentPinBase(QGraphicsWidget):

    def __init__(self, parent):
        super(UICommentPinBase, self).__init__(parent)
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.width = 8 + 1
        self.height = 8 + 1
        self.setGeometry(0, 0, self.width, self.height)
        self.expanded = True

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 8, 8)

    def sizeHint(self, which, constraint):
        try:
            return QtCore.QSizeF(self.width, self.height)
        except:
            return QGraphicsWidget.sizeHint(self, which, constraint)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        pass
        # PinPainter.asGroupPin(self, painter, option, widget)


class UIGroupPinBase(QGraphicsWidget):

    onCollapsed = QtCore.Signal(object)
    onExpanded = QtCore.Signal(object)

    def __init__(self, container):
        super(UIGroupPinBase, self).__init__()
        self._container = container
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.width = 8 + 1
        self.height = 8 + 1
        self.setGeometry(0, 0, self.width, self.height)
        self.expanded = True

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 8, 8)

    def sizeHint(self, which, constraint):
        try:
            return QtCore.QSizeF(self.width, self.height)
        except:
            return QGraphicsWidget.sizeHint(self, which, constraint)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        PinPainter.asGroupPin(self, painter, option, widget)

    def mousePressEvent(self, event):
        QGraphicsWidget.mousePressEvent(self, event)
        if self.expanded:
            self.onCollapsed.emit(self._container)
        else:
            self.onExpanded.emit(self._container)
        self.expanded = not self.expanded
        self.update()


class UIPinBase(QGraphicsWidget):
    '''
    Pin ui wrapper
    '''

    # Event called when pin is connected
    OnPinConnected = QtCore.Signal(object)
    # Event called when pin is disconnected
    OnPinDisconnected = QtCore.Signal(object)
    # Event called when data been set
    dataBeenSet = QtCore.Signal(object)
    # Event called when pin name changes
    nameChanged = QtCore.Signal(str)
    # Event called when pin name changes
    displayNameChanged = QtCore.Signal(str)
    # Event called when setUserStruct called
    # used by enums
    userStructChanged = QtCore.Signal(object)
    OnPinChanged = QtCore.Signal(object)
    OnPinDeleted = QtCore.Signal(object)

    def __init__(self, owningNode, raw_pin):
        super(UIPinBase, self).__init__()
        self._rawPin = raw_pin
        self._rawPin.setWrapper(self)
        self.setParentItem(owningNode)
        self.UiNode = weakref.ref(owningNode)
        # self.setCursor(QtCore.Qt.CrossCursor)
        # context menu for pin
        self.menu = QMenu()
        # Disconnect all connections
        self.actionDisconnect = self.menu.addAction('Disconnect all')
        self.actionDisconnect.triggered.connect(self.disconnectAll)
        # Copy UUID to buffer
        self.actionCopyUid = self.menu.addAction('Copy uid')
        self.actionCopyUid.triggered.connect(self.saveUidToClipboard)

        # label item weak ref
        self._label = None

        self.newPos = QtCore.QPointF()
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.width = 6 + 1
        self.height = 6 + 1
        self.hovered = False
        self.startPos = None
        self.endPos = None
        self._container = None
        self._groupContainer = None
        self._execPen = QtGui.QPen(Colors.White, 0.5, QtCore.Qt.SolidLine)
        self.setGeometry(0, 0, self.width, self.height)
        self._dirty_pen = QtGui.QPen(
            Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        self.pinImage = QtGui.QImage(':/icons/resources/array.png')
        self.bLabelHidden = False
        self.bAnimate = False
        self._val = 0
        self._displayName = self.name
        self._color = QtGui.QColor(*self._rawPin.color())
        self.uiConnectionList = []

    def setLabel(self, labelItem):
        if self._label is None:
            self._label = weakref.ref(labelItem)

    def getLabel(self):
        assert(self._label is not None)
        return self._label

    def displayName(self):
        return self._displayName

    def setDisplayName(self, displayName):
        self._displayName = displayName
        self.displayNameChanged.emit(self._displayName)

    @property
    def owningNode(self):
        return self.UiNode

    @property
    def constraint(self):
        return self._rawPin.constraint

    @property
    def isAny(self):
        return self._rawPin.isAny

    def setRenamingEnabled(self, bEnabled):
        self._rawPin.setRenamingEnabled(bEnabled)
        self._label()._isEditable = bEnabled
        actionsNames = [a.text() for a in self.menu.actions()]
        if bEnabled and "Rename" not in actionsNames:
            renameAction = self.menu.addAction("Rename")
            renameAction.triggered.connect(self.onRename)

    def canBeRenamed(self):
        return self._rawPin.canBeRenamed()

    def onRename(self):
        name, confirmed = QInputDialog.getText(
            None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            self.setName(name)
            self.setDisplayName(name)

    def setDynamic(self, bDynamic):
        self._rawPin.setDynamic(bDynamic)
        actionsNames = [a.text() for a in self.menu.actions()]
        if bDynamic and "Remove" not in actionsNames:
            removeAction = self.menu.addAction("Remove")
            removeAction.triggered.connect(self.kill)

    def isDynamic(self):
        return self._rawPin.isDynamic()

    @property
    def dirty(self):
        return self._rawPin.dirty

    @dirty.setter
    def dirty(self, value):
        self._rawPin.dirty = value

    def defaultValue(self):
        return self._rawPin.defaultValue()

    def getUserStruct(self):
        return self._rawPin.getUserStruct()

    def currentData(self):
        return self._rawPin.currentData()

    @property
    def name(self):
        return self._rawPin.name

    def getName(self):
        return self._rawPin.getName()

    def hasConnections(self):
        return self._rawPin.hasConnections()

    def setClean(self):
        self._rawPin.setClean()

    def setDirty(self):
        self._rawPin.setDirty()

    @property
    def _data(self):
        return self._rawPin._data

    @_data.setter
    def _data(self, value):
        self._rawPin._data = value

    @property
    def affects(self):
        return self._rawPin.affects

    @property
    def direction(self):
        return self._rawPin.direction

    @property
    def actLikeDirection(self):
        return self._rawPin.actLikeDirection

    @actLikeDirection.setter
    def actLikeDirection(self, value):
        self._rawPin.actLikeDirection = value

    @property
    def affected_by(self):
        return self._rawPin.affected_by

    def supportedDataTypes(self):
        return self._rawPin.supportedDataTypes()

    @property
    def connections(self):
        return self.uiConnectionList

    @property
    def uid(self):
        return self._rawPin._uid

    @uid.setter
    def uid(self, value):
        self._rawPin._uid = value

    def color(self):
        return self._color

    def setUserStruct(self, inStruct):
        self._rawPin.setUserStruct(inStruct)
        self.userStructChanged.emit(inStruct)

    def setName(self, newName):
        self._rawPin.setName(newName)
        self.nameChanged.emit(newName)

    def setData(self, value):
        self._rawPin.setData(value)
        self.dataBeenSet.emit(value)

    def getData(self):
        return self._rawPin.getData()

    def highlight(self):
        # TODO: draw svg arrow instead
        self.bAnimate = True
        t = QtCore.QTimeLine(900, self)
        t.setFrameRange(0, 100)
        t.frameChanged[int].connect(self.animFrameChanged)
        t.finished.connect(self.animationFinished)
        t.start()

    def animFrameChanged(self, value):
        self.width = clamp(math.sin(self._val) * 9, 4.5, 25)
        self.update()
        self._val += 0.1

    def animationFinished(self):
        self.width = 9
        self.update()
        self._val = 0

    def call(self):
        self._rawPin.call()
        for e in self.connections:
            e.highlight()

    def kill(self):
        self.disconnectAll()
        if self._container is not None:
            self.owningNode().graph().scene().removeItem(self._container)
            if not self._groupContainer:
                if self._rawPin.direction == PinDirection.Input:
                    self.owningNode().inputsLayout.removeItem(self._container)
                else:
                    self.owningNode().outputsLayout.removeItem(self._container)
            else:
                self.owningNode().graph().scene().removeItem(self._groupContainer)
                if self._rawPin.direction == PinDirection.Input:
                    self.owningNode().inputsLayout.removeItem(self._groupContainer)
                else:
                    self.owningNode().outputsLayout.removeItem(self._groupContainer)
        self._rawPin.kill()
        self.OnPinDeleted.emit(self)
        self.update()

    @staticmethod
    def deserialize(owningNode, jsonData):
        name = jsonData['name']
        dataType = jsonData['dataType']
        direction = jsonData['direction']
        value = jsonData['value']
        uid = uuid.UUID(jsonData['uuid'])
        bLabelHidden = jsonData['bLabelHidden']
        bDirty = jsonData['bDirty']

        p = None
        if direction == PinDirection.Input:
            p = owningNode.addInputPin(name, dataType, hideLabel=bLabelHidden)
            p.uid = uid
        else:
            p = owningNode.addOutputPin(name, dataType, hideLabel=bLabelHidden)
            p.uid = uid

        p.setData(value)
        return p

    def serialize(self):
        data = self._rawPin.serialize()
        data['bLabelHidden'] = self.bLabelHidden
        data['displayName'] = self.displayName()
        return data

    def ungrabMouseEvent(self, event):
        super(UIPinBase, self).ungrabMouseEvent(event)

    def getContainer(self):
        return self._container

    @property
    def dataType(self):
        return self._rawPin._dataType

    @dataType.setter
    def dataType(self, value):
        self._rawPin._dataType = value

    def boundingRect(self):
        if not self.dataType == 'ExecPin':
            return QtCore.QRectF(0, -0.5, 8 * 1.5, 8 + 1.0)
        else:
            return QtCore.QRectF(0, -0.5, 10 * 1.5, 10 + 1.0)

    def sizeHint(self, which, constraint):
        try:
            return QtCore.QSizeF(self.width, self.height)
        except:
            return QGraphicsWidget.sizeHint(self, which, constraint)

    def saveUidToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.clear()
        clipboard.setText(str(self.uid))

    def disconnectAll(self):
        if len(self.uiConnectionList) > 0:
            self.owningNode().graph().removeEdgeCmd(self.uiConnectionList)
        self.update()

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def isArray(self):
        return self._rawPin.isArray()

    def paint(self, painter, option, widget):
        if self.isArray():
            PinPainter.asArrayPin(self, painter, option, widget)
        else:
            PinPainter.asValuePin(self, painter, option, widget)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    def getLayout(self):
        if self.direction == PinDirection.Input:
            return self.owningNode().inputsLayout
        else:
            return self.owningNode().outputsLayout

    def hoverEnterEvent(self, event):
        super(UIPinBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        hoverMessage = "Data: {0}\r\nDirty: {1}".format(
            str(self._rawPin.currentData()), self._rawPin.dirty)
        self.setToolTip(hoverMessage)
        event.accept()

    def hoverLeaveEvent(self, event):
        super(UIPinBase, self).hoverLeaveEvent(event)
        self.update()
        self.hovered = False

    def pinConnected(self, other):
        self.OnPinConnected.emit(other)
        self.update()

    def pinDisconnected(self, other):
        self.OnPinDisconnected.emit(other)
        self.update()


def REGISTER_UI_PIN_FACTORY(packageName, factory):
    if packageName not in UI_PINS_FACTORIES:
        UI_PINS_FACTORIES[packageName] = factory
        print("registering", packageName, "ui pins")


def getUIPinInstance(owningNode, raw_instance):
    packageName = raw_instance.packageName()
    instance = None
    if packageName in UI_PINS_FACTORIES:
        instance = UI_PINS_FACTORIES[packageName](owningNode, raw_instance)
    assert(instance is not None)
    return instance