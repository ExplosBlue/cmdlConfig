from os import path
import xml.etree.ElementTree as ElementTree
import argparse
import pickle

class objProperties:
    def __init__(self):
        self.materials = []

    def addMaterial(self, material):
        self.materials.append(material)

def createPropertiesList(xmlRoot):
    propertiesList = objProperties()

    for material in xmlRoot.iter('MaterialCtr'):
            propertiesList.addMaterial(material)

    return propertiesList


def generateConfig():
    xmlTree = ElementTree.parse(args['infile'])
    xmlRoot = xmlTree.getroot()

    propertyList = createPropertiesList(xmlRoot)

    outPath = ''

    if args['outfile'] is None:
        outPath = path.splitext(args['infile'])[0] + '.conf'
    else:
        outPath = args['outfile']

    with open(outPath, 'wb') as outfile:
        pickle.dump(propertyList, outfile, pickle.HIGHEST_PROTOCOL)
    
    print('Generated config with {matCount} materials'.format(matCount=len(propertyList.materials)))



def setMaterialsFromConfig(xmlRoot, propertiesList):
    materialCount = 0

    for models in xmlRoot.iter('Models'):
        for model in models:
            for materials in model.iter('Materials'):

                for material in materials:

                    for mat in propertiesList.materials:

                        if material.attrib.get('Name') == mat.attrib.get('Name'):
                            materialCount += 1

                            materials.remove(material)
                            materials.append(mat)

    print('Updated {matCount} materials'.format(matCount=materialCount))


def applyConfig(configPath, outPath):
    with open(configPath, 'rb') as infile:
        propertiesList = pickle.load(infile)
        print(propertiesList)

    xmlTree = ElementTree.parse(args['infile'])
    xmlRoot = xmlTree.getroot()

    setMaterialsFromConfig(xmlRoot, propertiesList)

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



