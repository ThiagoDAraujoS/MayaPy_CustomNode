import math
from maya import OpenMaya, OpenMayaMPx
import maya.cmds as cmds

NODE_NAME = 'RobotSolver'
NODE_ID = OpenMaya.MTypeId(0x62115)
AUTHOR = "Thiago Silva"
VERSION = 0.1


class RobotSolver(OpenMayaMPx.MPxNode):
    frame_data_past    = OpenMaya.MObject()
    frame_data_present = OpenMaya.MObject()

    frequency = OpenMaya.MObject()
    dampening = OpenMaya.MObject()
    feedback  = OpenMaya.MObject()

    output  = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        if plug == RobotSolver.output:
            past      = data.inputValue(RobotSolver.frame_data_past).asFloat3()
            current   = data.inputValue(RobotSolver.frame_data_present).asFloat3()
            frequency = data.inputValue(RobotSolver.frequency).asFloat()
            damp      = data.inputValue(RobotSolver.dampening).asFloat()
            feedback  = data.inputValue(RobotSolver.feedback).asFloat()
            output    = data.outputValue(RobotSolver.output)

            """ Solution 1
            Check current time,
            If it is > than last saved time
                Integrate system and save new values
            Else
                reset integration
            """

            """
            Integrate the past X frames and merge their values
            """




            # compute constants
            k1 = damp / (math.pi * frequency)
            k2 = 1 / (2 * math.pi * frequency) ** 2
            k3 = feedback * damp / (2 * math.pi * frequency)



            data.outputValue(RobotSolver.output).set3Float(past[0], past[1], past[2])
            data.setClean(plug)


class SecondOrderDynamics:
    def __init__(self, f, z, r):
        # constants
        self.k1 = z / (math.pi * f)
        self.k2 = 1 / ((2 * math.pi * f) * (2 * math.pi * f))
        self.k3 = r * z / (2 * math.pi * f)

        # variables
        self.xp = (0, 0, 0)
        self.y = (0, 0, 0)
        self.yd = 0

    def update(self, T: float, x: OpenMaya.MVector, xd: OpenMaya.MVector = None):
        if xd == null:
            xd = (x - xp) / T
            self.xp = x
        self.y = self.y + T * self.yd
        self.yd = self.yd + T * (x + k3 * xd - y - k1 * self.yd) / k2
        return self.y


def create(): return OpenMayaMPx.asMPxPtr(RobotSolver())


def initializePlugin(mobject):
    m_plugin = OpenMayaMPx.MFnPlugin(mobject)
    m_plugin.registerNode(NODE_NAME, NODE_ID, create, initialize)


def uninitializePlugin(mobject):
    m_plugin = OpenMayaMPx.MFnPlugin(mobject)
    m_plugin.deregisterNode(NODE_ID)


def initialize():
    nAttr  = OpenMaya.MFnNumericAttribute()

    def set_plug_default_properties(isInput: bool) -> None:
        nAttr.setReadable(not isInput)
        nAttr.setWritable(isInput)
        nAttr.setKeyable(isInput)
        nAttr.setStorable(isInput)

    def create_point(is_input, short_name, long_name):
        plug = nAttr.createPoint(long_name, short_name)
        set_plug_default_properties(is_input)
        return plug

    def create_single(is_input, short_name, long_name):
        plug = nAttr.create(long_name, short_name, OpenMaya.MFnNumericData.kFloat, 0.5)
        set_plug_default_properties(is_input)
        return plug

    RobotSolver.frequency          = create_single(True, "htz", "frequency")
    RobotSolver.dampening          = create_single(True, "dp", "dampening")
    RobotSolver.feedback           = create_single(True, "fb", "feedback")
    RobotSolver.frame_data_past    = create_point(True, "pst", "past_frame_data")
    RobotSolver.frame_data_present = create_point(True, "cur", "present_frame_data")
    RobotSolver.output             = create_point(False, "out", "output")

    RobotSolver.addAttribute(RobotSolver.frequency)
    RobotSolver.addAttribute(RobotSolver.dampening)
    RobotSolver.addAttribute(RobotSolver.feedback)
    RobotSolver.addAttribute(RobotSolver.frame_data_past)
    RobotSolver.addAttribute(RobotSolver.frame_data_present)
    RobotSolver.addAttribute(RobotSolver.output)

    RobotSolver.attributeAffects(RobotSolver.frequency, RobotSolver.output)
    RobotSolver.attributeAffects(RobotSolver.dampening, RobotSolver.output)
    RobotSolver.attributeAffects(RobotSolver.feedback, RobotSolver.output)
    RobotSolver.attributeAffects(RobotSolver.frame_data_past, RobotSolver.output)
    RobotSolver.attributeAffects(RobotSolver.frame_data_present, RobotSolver.output)
