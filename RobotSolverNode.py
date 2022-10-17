import math
from maya import OpenMaya, OpenMayaMPx


def create():  # (2)
    return OpenMayaMPx.asMPxPtr(Circler())


nodeName = 'circler'  # (4)
nodeTypeID = OpenMaya.MTypeId(0x60005)  # (5)


def _toplugin(mobject):  # (6)
    return OpenMayaMPx.MFnPlugin(mobject, 'Marcus Reynir', '0.01')


def initializePlugin(mobject):
    plugin = _toplugin(mobject)
    plugin.registerNode(nodeName, nodeTypeID, create, init)


def uninitializePlugin(mobject):
    plugin = _toplugin(mobject)
    plugin.deregisterNode(nodeTypeID)


# Fleshing out in later sections

class Circler(OpenMayaMPx.MPxNode):
    inputFrame = OpenMaya.MObject()  # input
    frequency = OpenMaya.MObject()  # input
    scale = OpenMaya.MObject()  # input
    outSine = OpenMaya.MObject()  # output
    outCosine = OpenMaya.MObject()  # output

    def compute(self, plug, data):  # (1)
        if plug not in (Circler.outSine, Circler.outCosine):  # (2)
            return OpenMaya.MStatus.kUnknownParameter
        inputData = data.inputValue(Circler.input)  # (3)
        scaleData = data.inputValue(Circler.scale)
        framesData = data.inputValue(Circler.frames)

        inputVal = inputData.asFloat()  # (4)
        scaleFactor = scaleData.asFloat()
        framesPerCircle = framesData.asFloat()

        angle = 6.2831853 * (inputVal / framesPerCircle)  # (5)
        sinResult = math.sin(angle) * scaleFactor
        cosResult = math.cos(angle) * scaleFactor

        sinHandle = data.outputValue(Circler.outSine)  # (6)
        cosHandle = data.outputValue(Circler.outCosine)
        sinHandle.setFloat(sinResult)  # (7)
        cosHandle.setFloat(cosResult)
        data.setClean(plug)  # (8)
        return OpenMaya.MStatus.kSuccess  # (9)


def set_input(nAttr: OpenMaya.MFnNumericAttribute()):
    nAttr.setReadable(False)
    nAttr.setWritable(True)
    nAttr.setKeyable(True)
    nAttr.setStorable(True)


def set_output(nAttr: OpenMaya.MFnNumericAttribute()):
    nAttr.setReadable(True)
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setKeyable(False)


def init():
    nAttr = OpenMaya.MFnNumericAttribute()  # (1)
    kFloat = OpenMaya.MFnNumericData.kFloat

    # (2) Setup the input attributes
    Circler.input = nAttr.create('input', 'in', kFloat, 0.0)
    set_input(nAttr)

    Circler.scale = nAttr.create('scale', 'sc', kFloat, 10.0)
    set_input(nAttr)

    Circler.frames = nAttr.create('frames', 'fr', kFloat, 48.0)
    set_input(nAttr)

    # (3) Setup the output attributes
    Circler.outSine = nAttr.create('outSine', 'so', kFloat, 0.0)
    set_output(nAttr)

    Circler.outCosine = nAttr.create('outCosine', 'co', kFloat, 0.0)
    set_output(nAttr)

    # (4) Add the attributes to the node
    Circler.addAttribute(Circler.input)
    Circler.addAttribute(Circler.scale)
    Circler.addAttribute(Circler.frames)
    Circler.addAttribute(Circler.outSine)
    Circler.addAttribute(Circler.outCosine)

    # (5) Set the attribute dependencies
    Circler.attributeAffects(Circler.input, Circler.outSine)
    Circler.attributeAffects(Circler.input, Circler.outCosine)
    Circler.attributeAffects(Circler.scale, Circler.outSine)
    Circler.attributeAffects(Circler.scale, Circler.outCosine)
    Circler.attributeAffects(Circler.frames, Circler.outSine)
    Circler.attributeAffects(Circler.frames, Circler.outCosine)
