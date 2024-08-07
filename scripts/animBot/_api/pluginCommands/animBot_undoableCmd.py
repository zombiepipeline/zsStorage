




import sys
import _ctypes

import maya.OpenMayaMPx as OpenMayaMPx


o_____l_____0___o____1____1_____1__o_o__l___0_o___l__o__0____1____l__l___0___0___l_____l_l____0 = "animBot_undoableCmd"


class o__l_____0__o___0____o_____0_O___1____O__O___0_____l____o(OpenMayaMPx.MPxCommand):

    def isUndoable(o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O):
        
        return True

    def doIt(o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O, args):
        



        o__0___1__0_O__1 = long(args.asString(0), 0)
        o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o_O_1___0_1_____O____o__o_____O_____o____l_____l = _ctypes.PyObj_FromPtr(o__0___1__0_O__1)

        o_o___o____l___l____l = long(args.asString(1), 0)
        o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o__0_O_o__O_o____o_O_____l___0 = _ctypes.PyObj_FromPtr(o_o___o____l___l____l)

        if o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o__0_O_o__O_o____o_O_____l___0 is not None:
            o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o__0_O_o__O_o____o_O_____l___0.doIt()

    def redoIt(o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O):
        if o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o_O_1___0_1_____O____o__o_____O_____o____l_____l is not None:
            o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o_O_1___0_1_____O____o__o_____O_____o____l_____l.redoIt()

        if o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o__0_O_o__O_o____o_O_____l___0 is not None:
            o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o__0_O_o__O_o____o_O_____l___0.doIt()

    def undoIt(o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O):
        if o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o_O_1___0_1_____O____o__o_____O_____o____l_____l is not None:
            o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o_O_1___0_1_____O____o__o_____O_____o____l_____l.undoIt()

        if o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o__0_O_o__O_o____o_O_____l___0 is not None:
            o___l___1____1___l_____O_l_____1_0_____o__0___O_____0_o____O_O.o__0_O_o__O_o____o_O_____l___0.undoIt()




def cmdCreator():
    
    return OpenMayaMPx.asMPxPtr(o__l_____0__o___0____o_____0_O___1____O__O___0_____l____o())


def initializePlugin(o____o_____0____O_____O_1_____O___1):
    
    o__1__O_____1_____O_l____o_o_____O_____1___0____0___o___l_____l = OpenMayaMPx.MFnPlugin(o____o_____0____O_____O_1_____O___1, "animBot", "1.0", "Any")
    try:
        o__1__O_____1_____O_l____o_o_____O_____1___0____0___o___l_____l.registerCommand(o_____l_____0___o____1____1_____1__o_o__l___0_o___l__o__0____1____l__l___0___0___l_____l_l____0, cmdCreator)
    except:
        sys.stderr.write("Failed to register command: " + o_____l_____0___o____1____1_____1__o_o__l___0_o___l__o__0____1____l__l___0___0___l_____l_l____0)


def uninitializePlugin(o____o_____0____O_____O_1_____O___1):
    
    o__1__O_____1_____O_l____o_o_____O_____1___0____0___o___l_____l = OpenMayaMPx.MFnPlugin(o____o_____0____O_____O_1_____O___1)
    try:
        o__1__O_____1_____O_l____o_o_____O_____1___0____0___o___l_____l.deregisterCommand(o_____l_____0___o____1____1_____1__o_o__l___0_o___l__o__0____1____l__l___0___0___l_____l_l____0)
    except:
        sys.stderr.write("Failed to unregister command: " + o_____l_____0___o____1____1_____1__o_o__l___0_o___l__o__0____1____l__l___0___0___l_____l_l____0)


