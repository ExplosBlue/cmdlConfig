from os import path
import xml.etree.ElementTree as ElementTree
import argparse
import pickle

class objProperties:
    def __init__(self):
        self.materials = []
        self.meshes = []

    def addMaterial(self, material: ElementTree.Element):
        self.materials.append(material)

    def addMesh(self, mesh: ElementTree.Element):
        self.meshes.append(mesh)


def generateConfig():
    cmdlTree = ElementTree.parse(args['infile'])
    cmdlRoot = cmdlTree.getroot()

    propertyList = objProperties()

    # Add Materials to config
    for material in cmdlRoot.iter('MaterialCtr'):
        propertyList.addMaterial(material)

    # Add Meshes to config
    if args['meshes']:
        for mesh in cmdlRoot.iter('Mesh'):
            propertyList.addMesh(mesh)

    # Output the config file
    outPath = ''

    if args['outfile'] is None:
        outPath = path.splitext(args['infile'])[0] + '.conf'
    else:
        outPath = args['outfile']

    with open(outPath, 'wb') as outfile:
        pickle.dump(propertyList, outfile, pickle.HIGHEST_PROTOCOL)
    
    print('Generated config with:')
    print(' - {matCount} materials'.format(matCount=len(propertyList.materials)))
    print(' - {meshCount} meshes'.format(meshCount=len(propertyList.meshes)))


def setMaterialsFromConfig(cmdlRoot: ElementTree.Element, propertiesList: objProperties):

    # Get a list of all materials in the CMDL
    materialsIter = cmdlRoot.iter('MaterialCtr')
    materialsList = list(materialsIter)

    newMaterials = []

    matChangedCount = 0
    totalMaterials = len(materialsList)

    # Loop over each material in the materials list
    for material in materialsList:
        materialExists = False

        # Loop over each material in the properties list
        for mat in propertiesList.materials:

            # Compare material in CMDL with material in properties list
            if material.attrib.get('Name') == mat.attrib.get('Name'):

                # If material exists in both the CMDL and the Properties list, store the one from the properties list
                newMaterials.append(mat)
                matChangedCount += 1
                materialExists = True
                break
        
        # Material doesn't exist in our properties list, store the one from the CMDL instead
        if not materialExists:
            newMaterials.append(material)

    # Remove all materials from the CMDL and insert the ones from our new materials list
    for materials in cmdlRoot.iter('Materials'):
        for material in list(materials):

            for material in list(materials):
                materials.remove(material)

            for mat in newMaterials:
                materials.append(mat)

    print('Updated {c} of {t} Materials'.format(c=matChangedCount, t=totalMaterials))


def setMeshesFromConfig(cmdlRoot: ElementTree.Element, propertiesList: objProperties):

    # Get a list of all meshes in the CMDL
    meshIter = cmdlRoot.iter('Mesh')
    meshList = list(meshIter)

    meshChangedCount = 0
    
    totalMeshes = len(meshList)
    print(len(meshList))
    print(totalMeshes)

    # Loop over each mesh in the mesh list
    for mesh in meshList:
        print(mesh.attrib.get('MeshNodeName'))
        for pMesh in propertiesList.meshes:

            if mesh.attrib.get('MeshNodeName') == pMesh.attrib.get('MeshNodeName'):
                mesh.set('RenderPriority', pMesh.attrib.get('RenderPriority'))

                for userData in pMesh.iter('UserData'):
                    mesh.append(userData)

                meshChangedCount += 1
                
                break

    print('Updated {c} of {t} Meshes'.format(c=meshChangedCount, t=totalMeshes))


def applyConfig(configPath: str, outPath: str):
    with open(configPath, 'rb') as infile:
        propertiesList = pickle.load(infile)

    cmdlTree = ElementTree.parse(args['infile'])
    cmdlRoot = cmdlTree.getroot()

    setMaterialsFromConfig(cmdlRoot, propertiesList)

    if args['meshes']:
        setMeshesFromConfig(cmdlRoot, propertiesList)

    cmdlTree.write(outPath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Saves and loads configuration for CMDL files')
    parser.add_argument('infile', metavar='In', help='Input file')
    parser.add_argument('outfile', metavar='Out', nargs='?', help='Output file')
    parser.add_argument('--apply', metavar='Config', dest='apply', nargs=1, help='Applies a config file to a CMDL if enabled (default: stores CMDL config to file)')
    parser.add_argument('--m', dest='meshes', action='store_true', help='Stores/loads mesh data if enabled')

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



