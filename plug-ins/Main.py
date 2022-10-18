import math
from maya import OpenMaya, OpenMayaMPx

NODE_NAME = 'RobotSolver'
NODE_ID = OpenMaya.MTypeId(0x62115)
AUTHOR = "Thiago Silva"
VERSION = 0.1


class RobotSolver(OpenMayaMPx.MPxNode):
    #frame_data_vector  = OpenMaya.MObject()

    frame_data_past    = OpenMaya.MObject()
    frame_data_present = OpenMaya.MObject()
    frame_data_future  = OpenMaya.MObject()

    frame_data_output  = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        if plug == RobotSolver.output_data:
            past_handler    = data.inputValue(RobotSolver.past_frame_data)
            present_handler = data.inputValue(RobotSolver.present_frame_data)
            future_handler  = data.inputValue(RobotSolver.future_frame_data)

            output_handle   = data.outputValue(RobotSolver.output_data)

            past_data    = past_handler.asFloat()
            present_data = present_handler.asFloat()
            future_data  = future_handler.asFloat()

            result = 0  # <- here do math stuff and finish with result

            output_handle.setFloat(result)
            data.setClean(plug)


def create():
    return OpenMayaMPx.asMPxPtr(RobotSolver())


def initializePlugin(mobject):
    m_plugin = OpenMayaMPx.MFnPlugin(mobject)
    m_plugin.registerNode(NODE_NAME, NODE_ID, create, initialize)


def uninitializePlugin(mobject):
    m_plugin = OpenMayaMPx.MFnPlugin(mobject)
    m_plugin.deregisterNode(NODE_ID)


def set_plug_attributes(isInput, attr, short_name, long_name):
    plug = attr.create(long_name, short_name, OpenMaya.MFnNumericData.kFloat, 0.0)
    attr.setReadable(not isInput)
    attr.setWritable(isInput)
    attr.setKeyable(isInput)
    attr.setStorable(isInput)
    return plug


def initialize():
    nAttr  = OpenMaya.MFnNumericAttribute()
    #cAttr  = OpenMaya.MFnCompoundAttribute()

    #RobotSolver.frame_data_vector  = cAttr.create("vector",  "frame_data_vector")
    #attr.setReadable(False)
    #attr.setWritable(True)
    #attr.setKeyable(True)
    #attr.setStorable(True)

    RobotSolver.frame_data_past    = set_plug_attributes(True,  nAttr, "past",    "frame_data_past")
    RobotSolver.frame_data_present = set_plug_attributes(True,  nAttr, "present", "frame_data_present")
    RobotSolver.frame_data_future  = set_plug_attributes(True,  nAttr, "future",  "frame_data_future")
    RobotSolver.frame_data_output  = set_plug_attributes(False, nAttr, "output",  "frame_data_output")

    #RobotSolver.addAttribute(RobotSolver.frame_data_vector)
    RobotSolver.addAttribute(RobotSolver.frame_data_past)
    RobotSolver.addAttribute(RobotSolver.frame_data_present)
    RobotSolver.addAttribute(RobotSolver.frame_data_future)
    RobotSolver.addAttribute(RobotSolver.frame_data_output)

    #RobotSolver.attributeAffects(RobotSolver.frame_data_vector,  RobotSolver.frame_data_output)
    RobotSolver.attributeAffects(RobotSolver.frame_data_past,    RobotSolver.frame_data_output)
    RobotSolver.attributeAffects(RobotSolver.frame_data_present, RobotSolver.frame_data_output)
    RobotSolver.attributeAffects(RobotSolver.frame_data_future,  RobotSolver.frame_data_output)
