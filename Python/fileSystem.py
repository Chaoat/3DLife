import rule

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

if __name__ == '__main__':
    Rule = loadRule('Rules/conways.rule')
    print(Rule)