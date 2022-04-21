from ast import arg
from os import path
import string
import xml.etree.ElementTree as ElementTree
import argparse
import pickle

class modelObj:
    def __init__(self, name, materials):
        self.name = name
        self.materials = materials

def createModelList(xmlRoot):
    modelsList = []

    for models in xmlRoot.iter('Models'):
        for model in models:

            materialsList = []

            for material in model.iter('MaterialCtr'):
                materialsList.append(material)

            modelsList.append(modelObj(model.attrib.get('Name'), materialsList))

    return modelsList


def generateConfig():
        xmlTree = ElementTree.parse(args['infile'])
        xmlRoot = xmlTree.getroot()

        outPath = ''

        if args['outfile'] is None:
            outPath = path.splitext(args['infile'])[0] + '.conf'
        else:
            outPath = args['outfile']

        with open(outPath, 'wb') as outfile:
            pickle.dump(createModelList(xmlRoot), outfile, pickle.HIGHEST_PROTOCOL)


def setMaterialsFromConfig(xmlRoot, modelsList):
    modelCount = 0
    materialCount = 0

    for models in xmlRoot.iter('Models'):

        for model in models:

            for mdl in modelsList:

                if model.attrib.get('Name') == mdl.name:
                    modelCount += 1

                    for materials in model.iter('Materials'):

                        for material in materials:

                            for mat in mdl.materials:

                                if material.attrib.get('Name') == mat.attrib.get('Name'):
                                    materialCount += 1

                                    materials.remove(material)
                                    materials.append(mat)

    print('Updated {matCount} materials in {mdlCount} models'.format(matCount=materialCount, mdlCount=modelCount))


def applyConfig(configPath, outPath):
    with open(configPath, 'rb') as infile:
        modelsList = pickle.load(infile)
        print(modelsList)

    xmlTree = ElementTree.parse(args['infile'])
    xmlRoot = xmlTree.getroot()

    setMaterialsFromConfig(xmlRoot, modelsList)

    xmlTree.write(outPath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Saves and loads configuration for CMDL files')
    parser.add_argument('infile', metavar='In', help='Input file')
    parser.add_argument('outfile', metavar='Out', nargs='?', help='Output file')
    parser.add_argument('--apply', metavar='Config', dest='apply', nargs=1, help='Applies a config file to a CMDL if enabled (default: stores CMDL config to file)')

    args = vars(parser.parse_args())

    if args['apply']:

        outPath = ''

        if args['outfile'] is None:
            outPath = path.splitext(args['infile'])[0] + '.cmdl'
        else:
            outPath = args['outfile']

        applyConfig(args['apply'][0], outPath)
    else:
        generateConfig()



