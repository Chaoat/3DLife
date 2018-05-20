class Rule:
    def __init__(self, moorelian, neighbourhoodLength, nStates, center, ndimensions):
        #https://en.wikipedia.org/wiki/Moore_neighborhood
        self.moorelian = moorelian
        self.dimensions = ndimensions
        self.neighbourhoodLength = neighbourhoodLength
        self.nStates = nStates
        self.center = center
        self.centerN = 0
        for i in range(0, len(center)):
            multiple = neighbourhoodLength**(len(center) - i - 1)
            self.centerN = self.centerN + multiple*center[i]
        self.decisionTree = [None]*nStates

    def convertToNeighbourhoodString(self, neighbourhood):
        neighbourString = self.convertToNeighbourhoodStringAux(neighbourhood)
        return neighbourString[:self.centerN] + neighbourString[(self.centerN + 1):]

    def convertToNeighbourhoodStringAux(self, neighbourhood):
        if isinstance(neighbourhood, int):
            return str(neighbourhood)
        else:
            linestring = ''
            for i in neighbourhood:
                linestring = linestring + self.convertToNeighbourhoodStringAux(i)
            return linestring

    def addRule(self, stateFunction, neighbourhood):
        neighbourhood = self.convertToNeighbourhoodString(neighbourhood)
        self.addRuleaux(self.decisionTree, stateFunction, neighbourhood)

    def addRuleaux(self, decisionTree, stateFunction, neighbourhood):
        if len(neighbourhood) > 1:
            if decisionTree[int(neighbourhood[0])] is None:
                decisionTree[int(neighbourhood[0])] = [None] * self.nStates
            self.addRuleaux(decisionTree[int(neighbourhood[0])], stateFunction, neighbourhood[1:])
        else:
            decisionTree[int(neighbourhood[0])] = stateFunction

if __name__ == '__main__':
    TestRule = Rule(True, 3, 2, [1, 1], 2)
    neighbourhood = [[1, 0, 0], [1, 0, 1], [0, 0, 1]]
    TestRule.addRule(True, neighbourhood)