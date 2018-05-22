class Rule:
    def __init__(self, moorelian, neighbourhoodLength, nStates, center, ndimensions, baseFunction):
        #https://en.wikipedia.org/wiki/Moore_neighborhood
        self.moorelian = moorelian
        self.ndimensions = ndimensions
        self.neighbourhoodLength = neighbourhoodLength
        self.nStates = nStates
        self.center = center
        self.centerN = 0
        for i in range(0, len(center)):
            multiple = neighbourhoodLength**(len(center) - i - 1)
            self.centerN = self.centerN + multiple*center[i]

        self.decisionTree = self.innitiateDecisionTree(neighbourhoodLength**ndimensions - 1, baseFunction)

    def innitiateDecisionTree(self, n, baseFunction):
        if n == 0:
            return baseFunction
        else:
            decisionTree = []
            for i in range(0, self.nStates):
                decisionTree.append(self.innitiateDecisionTree(n - 1, baseFunction))
            return decisionTree

    def convertToNeighbourhoodString(self, neighbourhood):
        neighbourString = self.convertToNeighbourhoodStringAux(neighbourhood)
        return neighbourString[:self.centerN] + neighbourString[(self.centerN + 1):]

    def convertToNeighbourhoodStringAux(self, neighbourhood):
        if isinstance(neighbourhood, int):
            return [neighbourhood]
        else:
            linestring = []
            for i in neighbourhood:
                linestring = linestring + self.convertToNeighbourhoodStringAux(i)
            return linestring

    def addRule(self, neighbours, stateFunction):
        self.addRuleaux(neighbours, stateFunction, self.decisionTree, self.neighbourhoodLength**self.ndimensions - 1)

    def addRuleaux(self, neighbours, stateFunction, decisionTree, depth):
        totalNeighbours = 0
        for neighbour in neighbours:
            totalNeighbours = totalNeighbours + neighbour

        if depth > 1:
            for i in range(0, len(neighbours) + 1):
                if i == 0:
                    self.addRuleaux(neighbours, stateFunction, decisionTree[0], depth - 1)
                elif neighbours[i - 1] > 0:
                    newNeighbours = []
                    for j in range(0, len(neighbours)):
                        n = neighbours[j]
                        if j == i - 1:
                            n = n - 1
                        newNeighbours.append(n)
                    self.addRuleaux(newNeighbours, stateFunction, decisionTree[i], depth - 1)
        elif totalNeighbours <= 1:
            slot = 0
            for i in range(0, len(neighbours)):
                if neighbours[i] == 1:
                    slot = i + 1
                    totalNeighbours = totalNeighbours - 1
                    break
            if totalNeighbours == 0:
                decisionTree[slot] = stateFunction

    def addRuleFromNeighbourhood(self, neighbourhood, stateFunction):
        neighbourhoodString = self.convertToNeighbourhoodString(neighbourhood)
        self.addRuleFromNeighbourhoodaux(self.decisionTree, stateFunction, neighbourhood)

    def addRuleFromNeighbourhoodaux(self, decisionTree, stateFunction, neighbourhoodString):
        if len(neighbourhoodString) > 1:
            self.addRuleFromNeighbourhoodaux(decisionTree[int(neighbourhoodString[0])], stateFunction, neighbourhoodString[1:])
        else:
            decisionTree[int(neighbourhoodString[0])] = stateFunction

if __name__ == '__main__':
    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthFunction(state):
        return 1
    TestRule = Rule(True, 3, 2, [1, 1], 2, dieFunction)
    TestRule.addRule([2], stayFunction)
    TestRule.addRule([3], birthFunction)