import math
import maya.OpenMaya as om
from maya import OpenMayaMPx


NODE_NAME = 'RobotSolver'
NODE_ID   = om.MTypeId(0x62115)
AUTHOR    = "Thiago Silva"
VERSION   = 0.1
AXIS      = ["X", "Y", "Z"]


class RobotSolver(OpenMayaMPx.MPxNode):
    frame_data_past    = OpenMaya.MObject()
    frame_data_present = OpenMaya.MObject()

    frequency = OpenMaya.MObject()
    dampening = OpenMaya.MObject()
    feedback  = OpenMaya.MObject()

    output  = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        cAttr.setReadable(not is_input)
        cAttr.setWritable(is_input)
        cAttr.setKeyable(is_input)
        cAttr.setStorable(is_input)

    def connect_to_vector_output(self, target_vector) -> None:
        for attribute in self.values:
            self.attribute_affects(attribute, target_vector.compound)

    def connect_to_single_output(self, target_output: om.MObject) -> None:
        for attribute in self:
            self.attribute_affects(attribute, target_output)

    def get_data(self, data):
        handles = [data.inputValue(attribute) for attribute in self.values]
        return handles[0].asFloat(), handles[1].asFloat(), handles[2].asFloat()

    def set_data(self, data, value: om.MVector) -> None:
        handles = [data.outputValue(attribute) for attribute in self.values]
        for handle, v in zip(handles, value):
            print(f"setting handle with value {str(v)}")
            handle.setFloat(v)


class RobotSolver(OpenMayaMPx.MPxNode):
    past_frame_data    = VectorAttribute()
    current_frame_data = VectorAttribute()
    output_data        = VectorAttribute()

    def __init__(self): OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        if plug == RobotSolver.output:
            handle_past    = data.inputValue(RobotSolver.frame_data_past)
            handle_current = data.inputValue(RobotSolver.frame_data_present)
            handle_output  = data.outputValue(RobotSolver.output)

            d_past    = handle_past.asFloat3()
            d_current = handle_current.asFloat3()

            result = SecondOrderDynamics()

            handle_x.setFloat(2)
            handle_y.setFloat(4)
            handle_z.setFloat(6)

            handle_output.set3Float(d_past[0], d_past[1], d_past[2])
            data.setClean(plug)

        elif plug == RobotSolver.output_data.values[0]:
            print("I am triggering value X")
        elif plug == RobotSolver.output_data.values[1]:
            print("I am triggering value Y")
        elif plug == RobotSolver.output_data.values[2]:
            print("I am triggering value Z")

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
        plug = nAttr.create(long_name, short_name, OpenMaya.MFnNumericData.kFloat)
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
