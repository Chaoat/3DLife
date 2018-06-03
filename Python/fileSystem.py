import rule
import map
import math

def getBaseActions():
    actions = {}

    def dieFunction(state):
        return 0
    actions['die'] = dieFunction

    def stayFunction(state):
        return state
    actions['stay'] = stayFunction

    def birthFunction(state):
        if state == 0:
            return 1
        return state
    actions['birth'] = birthFunction

    def staybirthFunction(state):
        if state == 0:
            return 1
        return state
    actions['stay&birth'] = staybirthFunction

    return actions

def loadRule(directory):
    rawFile = open(directory)
    text = rawFile.read()
    lineList = text.split('\n')

    propertiesList = []
    for line in lineList:
        if line != '':
            property = line.split(':')
            if property[1] == 'TRUE':
                property[1] = True
            elif property[1] == 'FALSE':
                property[1] = False
            propertiesList.append(property)

    for i in range(5, len(propertiesList)):
        propertiesList[i][0] = propertiesList[i][0].split(', ')
        for j in range(0, len(propertiesList[i][0])):
            propertiesList[i][0][j] = int(propertiesList[i][0][j])

    center = propertiesList[3][1].split(', ')
    for i in range(0, len(center)):
        center[i] = int(center[i])

    actionTable = getBaseActions()

    loadedRule = rule.Rule(propertiesList[0][1], int(propertiesList[1][1]), int(propertiesList[2][1]), center, False, actionTable[propertiesList[4][1]])

    for i in range(5, len(propertiesList)):
        loadedRule.addRule(propertiesList[i][0], actionTable[propertiesList[i][1]])

    return loadedRule

def loadMap(directory):
    rawFile = open(directory)
    text = rawFile.read()
    lineList = text.split('\n')

    dimensions = lineList[1].split(',')
    for i in range(0, len(dimensions)):
        dimensions[i] = int(dimensions[i])

    dimensionMultipliers = []
    for i in range(0, len(dimensions)):
        dimensionMultipliers.append(1)
        for j in range(i + 1, len(dimensions)):
            dimensionMultipliers[i] = dimensionMultipliers[i]*dimensions[j]

    wrap = []
    wrapText = lineList[3].split(',')
    for i in range(0, len(wrapText)):
        if wrapText[i] == '1':
            wrap.append(True)
        else:
            wrap.append(False)

    outerState = int(lineList[2])

    loadedMap = map.Map(dimensions, wrap, outerState)
    textMap = lineList[0].split(',')
    for i in range(0, len(textMap)):
        position = []
        for j in range(0, len(dimensions)):
            position.append(math.floor(i/dimensionMultipliers[j])%dimensions[j])
        loadedMap[position] = int(textMap[i])

    return loadedMap

if __name__ == '__main__':
    Map = loadMap('Maps/3Dtest.map')
    print(Map)
    Map.print3D()