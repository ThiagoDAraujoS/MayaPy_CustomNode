import math
from maya import OpenMaya, OpenMayaMPx
from maya.OpenMaya import MVector as Vector

NODE_NAME = 'RobotSolver'
NODE_ID = OpenMaya.MTypeId(0x62115)
AUTHOR = "Thiago Silva"
VERSION = 0.1


class VectorAttribute:
    def __init__(self, is_input, short_name, long_name):
        self.compound = OpenMaya.MObject()
        self.x, self.y, self.z = OpenMaya.MObject(), OpenMaya.MObject(), OpenMaya.MObject()
        self.long_name  = long_name
        self.short_name = short_name
        self.is_input   = is_input

    def __iter__(self): yield from [self.compound, self.x, self.y, self.z]

    def initialize_vector(self, uAttr, cAttr):
        self.compound = cAttr.create(self.long_name, self.short_name)
        self.x = uAttr.create(f'{self.long_name}X', f'{self.short_name}X', OpenMaya.MFnUnitAttribute.kDistance)
        self.y = uAttr.create(f'{self.long_name}Y', f'{self.short_name}Y', OpenMaya.MFnUnitAttribute.kDistance)
        self.z = uAttr.create(f'{self.long_name}Z', f'{self.short_name}Z', OpenMaya.MFnUnitAttribute.kDistance)

        cAttr.addChild(self.x)
        cAttr.addChild(self.y)
        cAttr.addChild(self.z)

        cAttr.setReadable(not self.is_input)
        cAttr.setWritable(self.is_input)
        cAttr.setKeyable(self.is_input)
        cAttr.setStorable(self.is_input)

    def connect_all_to_output(self, affects_function, target_output):
        for attribute in self:
            affects_function(attribute, target_output)

    def connect_input_to_all(self, affects_function, target_input):
        for attribute in self:
            affects_function(target_input, attribute)

    def connect_to_output_vector(self, affects_function, target_output_vector):
        for attribute in target_output_vector:
            self.connect_all_to_output(affects_function, attribute)

    def get_data(self, data) -> Vector:
        result = Vector(
            data.inputValue(self.x).asFloat(),
            data.inputValue(self.y).asFloat(),
            data.inputValue(self.z).asFloat())
        return result

    def set_data(self, data, value: Vector):
        data.inputValue(self.x).setFloat(value.x)
        data.inputValue(self.y).setFloat(value.y)
        data.inputValue(self.z).setFloat(value.z)


class RobotSolver(OpenMayaMPx.MPxNode):
    past_frame_data    = VectorAttribute(True,  "p", "past_data")
    current_frame_data = VectorAttribute(True,  "d", "data")
    output_data        = VectorAttribute(False, "o", "output")

    def __init__(self): OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        if plug in RobotSolver.output_data:
            oHX = data.outputValue(RobotSolver.output_data.x)
            oHY = data.outputValue(RobotSolver.output_data.y)
            oHZ = data.outputValue(RobotSolver.output_data.z)
            oHX.setFloat(1)
            oHY.setFloat(2)
            oHZ.setFloat(3)

            """past_data = RobotSolver.past_frame_data.get_data(data)
            curr_data = RobotSolver.current_frame_data.get_data(data)
            # print(f"{past_data.x} {past_data.y} {past_data.z}")
            # print(f"{curr_data.x} {curr_data.y} {curr_data.z}")
            RobotSolver.output_data.set_data(data, Vector(0, 0, 0))
            data.setClean()"""

       # past_handler    = data.inputValue(RobotSolver.past_frame_data)
       # present_handler = data.inputValue(RobotSolver.present_frame_data)
       # future_handler  = data.inputValue(RobotSolver.future_frame_data)

       # output_handle   = data.outputValue(RobotSolver.output_data)

       # past_data    = past_handler.asFloat()
       # present_data = present_handler.asFloat()
       # future_data  = future_handler.asFloat()

       # result = 0  # <- here do math stuff and finish with result

       # output_handle.setFloat(result)
       # data.setClean(plug)


def create(): return OpenMayaMPx.asMPxPtr(RobotSolver())


def initializePlugin(mobject):
    m_plugin = OpenMayaMPx.MFnPlugin(mobject)
    m_plugin.registerNode(NODE_NAME, NODE_ID, create, initialize)


def uninitializePlugin(mobject):
    m_plugin = OpenMayaMPx.MFnPlugin(mobject)
    m_plugin.deregisterNode(NODE_ID)


def initialize():
    cAttr = OpenMaya.MFnCompoundAttribute()
    uAttr = OpenMaya.MFnUnitAttribute()

    RobotSolver.past_frame_data.initialize_vector(uAttr, cAttr)
    RobotSolver.current_frame_data.initialize_vector(uAttr, cAttr)
    RobotSolver.output_data.initialize_vector(uAttr, cAttr)

    RobotSolver.addAttribute(RobotSolver.past_frame_data.compound)
    RobotSolver.addAttribute(RobotSolver.current_frame_data.compound)
    RobotSolver.addAttribute(RobotSolver.output_data.compound)

    RobotSolver.past_frame_data.connect_to_output_vector(RobotSolver.attributeAffects, RobotSolver.output_data)
    RobotSolver.current_frame_data.connect_to_output_vector(RobotSolver.attributeAffects, RobotSolver.output_data)

