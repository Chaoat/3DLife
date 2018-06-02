import rule

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
    return propertiesList
    #loadedRule = rule.Rule()

if __name__ == '__main__':
    Rule = loadRule('Rules\conways.rule')
    print(Rule)