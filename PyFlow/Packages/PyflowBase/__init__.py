PACKAGE_NAME = 'PyflowBase'

from PyFlow.Core.Interfaces import IPackage

# Pins
from PyFlow.Packages.PyflowBase.Pins.AnyPin import AnyPin
from PyFlow.Packages.PyflowBase.Pins.BoolPin import BoolPin
# TODO: Enums not working for now, fix this.
from PyFlow.Packages.PyflowBase.Pins.EnumPin import EnumPin
from PyFlow.Packages.PyflowBase.Pins.ExecPin import ExecPin
from PyFlow.Packages.PyflowBase.Pins.FloatPin import FloatPin
from PyFlow.Packages.PyflowBase.Pins.IntPin import IntPin
from PyFlow.Packages.PyflowBase.Pins.StringPin import StringPin
from PyFlow.Packages.PyflowBase.Pins.ListPin import ListPin

# Function based nodes
from PyFlow.Packages.PyflowBase.FunctionLibraries.ArrayLib import ArrayLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.BoolLib import BoolLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.DefaultLib import DefaultLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.FloatLib import FloatLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.IntLib import IntLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.MathLib import MathLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.MathAbstractLib import MathAbstractLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.RandomLib import RandomLib

# Class based nodes
from PyFlow.Packages.PyflowBase.Nodes.branch import branch
from PyFlow.Packages.PyflowBase.Nodes.charge import charge
from PyFlow.Packages.PyflowBase.Nodes.delay import delay
from PyFlow.Packages.PyflowBase.Nodes.deltaTime import deltaTime
from PyFlow.Packages.PyflowBase.Nodes.doN import doN
from PyFlow.Packages.PyflowBase.Nodes.doOnce import doOnce
from PyFlow.Packages.PyflowBase.Nodes.flipFlop import flipFlop
from PyFlow.Packages.PyflowBase.Nodes.forLoop import forLoop
from PyFlow.Packages.PyflowBase.Nodes.forLoopWithBreak import forLoopWithBreak
from PyFlow.Packages.PyflowBase.Nodes.implicitPinCall import implicitPinCall
from PyFlow.Packages.PyflowBase.Nodes.retriggerableDelay import retriggerableDelay
from PyFlow.Packages.PyflowBase.Nodes.sequence import sequence
from PyFlow.Packages.PyflowBase.Nodes.switchOnString import switchOnString
from PyFlow.Packages.PyflowBase.Nodes.timer import timer
from PyFlow.Packages.PyflowBase.Nodes.whileLoop import whileLoop
from PyFlow.Packages.PyflowBase.Nodes.commentNode import commentNode
from PyFlow.Packages.PyflowBase.Nodes.getVar import getVar
from PyFlow.Packages.PyflowBase.Nodes.setVar import setVar

_FOO_LIBS = {
    ArrayLib.__name__: ArrayLib(PACKAGE_NAME),
    BoolLib.__name__: BoolLib(PACKAGE_NAME),
    DefaultLib.__name__: DefaultLib(PACKAGE_NAME),
    FloatLib.__name__: FloatLib(PACKAGE_NAME),
    IntLib.__name__: IntLib(PACKAGE_NAME),
    MathLib.__name__: MathLib(PACKAGE_NAME),
    MathAbstractLib.__name__: MathAbstractLib(PACKAGE_NAME),
    RandomLib.__name__: RandomLib(PACKAGE_NAME),
}

_NODES = {
    branch.__name__: branch,
    charge.__name__: charge,
    delay.__name__: delay,
    deltaTime.__name__: deltaTime,
    doN.__name__: doN,
    doOnce.__name__: doOnce,
    flipFlop.__name__: flipFlop,
    forLoop.__name__: forLoop,
    forLoopWithBreak.__name__: forLoopWithBreak,
    implicitPinCall.__name__: implicitPinCall,
    retriggerableDelay.__name__: retriggerableDelay,
    sequence.__name__: sequence,
    switchOnString.__name__: switchOnString,
    timer.__name__: timer,
    whileLoop.__name__: whileLoop,
    commentNode.__name__: commentNode,
    getVar.__name__: getVar,
    setVar.__name__: setVar
}

_PINS = {
    AnyPin.__name__: AnyPin,
    BoolPin.__name__: BoolPin,
    EnumPin.__name__: EnumPin,
    ExecPin.__name__: ExecPin,
    FloatPin.__name__: FloatPin,
    IntPin.__name__: IntPin,
    StringPin.__name__: StringPin,
    ListPin.__name__: ListPin
}


class PyflowBase(IPackage):
    def __init__(self):
        super(PyflowBase, self).__init__()

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        return _NODES

    @staticmethod
    def GetPinClasses():
        return _PINS