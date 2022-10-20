import math
import maya.OpenMaya as om
from maya import OpenMayaMPx


NODE_NAME = 'RobotSolver'
NODE_ID   = om.MTypeId(0x62115)
AUTHOR    = "Thiago Silva"
VERSION   = 0.1
AXIS      = ["X", "Y", "Z"]


class VectorAttribute:
    def __init__(self):
        self.compound: om.MObject = om.MObject()
        self.values: om.MObject = [om.MObject(), om.MObject(), om.MObject()]
        self.attribute_affects = None

    def __iter__(self) -> om.MObject:
        yield self.compound
        yield from self.values

    def initialize(self, uAttr:  om.MFnUnitAttribute, cAttr: om.MFnCompoundAttribute, long_name: str, short_name: str, is_input: bool, attribute_affects) -> None:
        self.attribute_affects = attribute_affects
        self.compound = cAttr.create(long_name, short_name)

        for i in range(len(self.values)):
            self.values[i] = uAttr.create(f'{long_name}{AXIS[i]}', f'{short_name}{AXIS[i]}', om.MFnUnitAttribute.kDistance)
            cAttr.addChild(self.values[i])

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
        if plug == RobotSolver.output_data.compound:
            print("output compound was triggered")
            past_vector = RobotSolver.past_frame_data.get_data(data)
            curr_vector = RobotSolver.current_frame_data.get_data(data)

            print(f"curr_vector = {str(curr_vector[0])} {str(curr_vector[1])} {str(curr_vector[2])}")
            print(f"past_vector = {str(past_vector[0])} {str(past_vector[1])} {str(past_vector[2])}")

            handle_x = data.outputValue(RobotSolver.output_data.values[0])
            handle_y = data.outputValue(RobotSolver.output_data.values[1])
            handle_z = data.outputValue(RobotSolver.output_data.values[2])

            handle_x.setFloat(2)
            handle_y.setFloat(4)
            handle_z.setFloat(6)

            data.setClean(plug)

        elif plug == RobotSolver.output_data.values[0]:
            print("I am triggering value X")
        elif plug == RobotSolver.output_data.values[1]:
            print("I am triggering value Y")
        elif plug == RobotSolver.output_data.values[2]:
            print("I am triggering value Z")


def create(): return OpenMayaMPx.asMPxPtr(RobotSolver())


def initializePlugin(mobject):
    m_plugin = OpenMayaMPx.MFnPlugin(mobject)
    m_plugin.registerNode(NODE_NAME, NODE_ID, create, initialize)


def uninitializePlugin(mobject):
    m_plugin = OpenMayaMPx.MFnPlugin(mobject)
    m_plugin.deregisterNode(NODE_ID)


def initialize():
    cAttr = om.MFnCompoundAttribute()
    uAttr = om.MFnUnitAttribute()

    RobotSolver.past_frame_data.initialize(uAttr, cAttr, "past_data", "p", True, RobotSolver.attributeAffects)
    RobotSolver.current_frame_data.initialize(uAttr, cAttr, "data", "d", True, RobotSolver.attributeAffects)
    RobotSolver.output_data.initialize(uAttr, cAttr, "output", "o", False, RobotSolver.attributeAffects)

    RobotSolver.addAttribute(RobotSolver.past_frame_data.compound)
    RobotSolver.addAttribute(RobotSolver.current_frame_data.compound)
    RobotSolver.addAttribute(RobotSolver.output_data.compound)

    RobotSolver.past_frame_data.connect_to_vector_output(RobotSolver.output_data)
    RobotSolver.current_frame_data.connect_to_vector_output(RobotSolver.output_data)
