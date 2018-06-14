import math

class Rule:
    def __init__(self, moorelian, neighbourhoodLength, nStates, center, useCenter, useDecisionTree, baseFunction):
        #https://en.wikipedia.org/wiki/Moore_neighborhood
        self.moorelian = moorelian
        self.ndimensions = len(center)
        self.neighbourhoodLength = neighbourhoodLength
        self.nStates = nStates
        self.center = center
        self.useCenter = useCenter

        if self.moorelian:
            self.neighbourhoodSize = self.neighbourhoodLength**self.ndimensions
            if self.useCenter:
                self.neighbourhoodSize = self.neighbourhoodSize + 1
        else:
            self.neumannRange = math.floor(self.neighbourhoodLength/2)
            self.neighbourhoodSize = self.findNeumannNeighbourhoodSize([])
            if self.useCenter:
                self.neighbourhoodSize = self.neighbourhoodSize + 1

        self.decisionTreeUsed = useDecisionTree
        if useDecisionTree:
            self.decisionTree = []
            for i in range(0, nStates):
                self.decisionTree.append(self.innitiateDecisionTree(self.findNeighbourhoodSize() - 1, baseFunction))
        else:
            self.neighbourTree = []
            for i in range(0, nStates):
                self.neighbourTree.append(self.innitiateNeighbourTree(self.findNeighbourhoodSize() + 1, nStates - 1, baseFunction))

    def findNeumannNeighbourhoodSize(self, coords):
        if len(coords) == self.ndimensions:
            return self.findNeumannDistance(coords)
        else:
            total = 0
            for i in range(0, self.neighbourhoodLength):
                total = total + self.findNeumannNeighbourhoodSize(coords + [i])
            return total

    def findNeighbourhoodSize(self):
        return self.neighbourhoodSize

    def findNeumannDistance(self, coords):
        difference = 0
        for i in range(0, len(coords)):
            difference = difference + math.fabs(coords[i] - self.center[i])
        if difference > self.neumannRange:
            return False
        return True

    def innitiateDecisionTree(self, n, baseFunction):
        if n == 0:
            return baseFunction
        else:
            decisionTree = []
            for i in range(0, self.nStates):
                decisionTree.append(self.innitiateDecisionTree(n - 1, baseFunction))
            return decisionTree

    def innitiateNeighbourTree(self, n, depth, baseFunction):
        if depth == 0:
            return baseFunction
        else:
            neighbourTree = []
            for i in range(0, n):
                neighbourTree.append(self.innitiateNeighbourTree(n, depth - 1, baseFunction))
            return neighbourTree

    def convertToNeighbourhoodString(self, neighbourhood):
        neighbourString = self.convertToNeighbourhoodStringAux(neighbourhood)
        return neighbourString

    def convertToNeighbourhoodStringAux(self, neighbourhood):
        if isinstance(neighbourhood, int):
            return [neighbourhood]
        else:
            linestring = []
            for i in neighbourhood:
                linestring = linestring + self.convertToNeighbourhoodStringAux(i)
            return linestring

    def addRule(self, centerState, neighbours, stateFunction):
        if self.decisionTreeUsed:
            self.addRuleaux(neighbours, stateFunction, self.decisionTree[centerState], self.findNeighbourhoodSize() - 1)
        else:
            self.addRuleTreelessaux(self.neighbourTree[centerState], neighbours, 0, stateFunction)

    def addRuleTreelessaux(self, position, neighbours, i, stateFunction):
        for j in range(neighbours[i][0], neighbours[i][1] + 1):
            if i == self.nStates - 2:
                position[j] = stateFunction
            else:
                self.addRuleTreelessaux(position[j], neighbours, i + 1, stateFunction)

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

    def addRuleFromNeighbourhood(self, centerState, neighbourhood, stateFunction):
        if self.decisionTreeUsed:
            self.addRuleFromNeighbourhoodaux(self.decisionTree[centerState], stateFunction, neighbourhood)
        else:
            nNeighbours = [0] * (self.nStates - 1)
            for neighbour in neighbourhoodString:
                if neighbour > 0:
                    nNeighbours[neighbour - 1] = nNeighbours[neighbour - 1] + 1

            i = 0
            position = self.neighbourTree
            while i < self.nStates - 1:
                if i == self.nStates - 2:
                    position[nNeighbours[i]] = stateFunction
                else:
                    position = position[nNeighbours[i]]
                i = i + 1

    def addRuleFromNeighbourhoodaux(self, decisionTree, stateFunction, neighbourhoodString):
        if len(neighbourhoodString) > 1:
            self.addRuleFromNeighbourhoodaux(decisionTree[int(neighbourhoodString[0])], stateFunction, neighbourhoodString[1:])
        else:
            decisionTree[int(neighbourhoodString[0])] = stateFunction

    def processMap(self, map):
        dimensions = map.getDimensions()
        if len(dimensions) == self.ndimensions:
            newMap = map.duplicateMap()
            cellsToCheck = map.findAllCells()
            for cell in cellsToCheck:
                centerState = cell[1]
                neighbourList = self.convertToNeighbourhoodString(self.findNeighbourList(cell[0], map))
                function = self.determineAction(neighbourList, centerState)
                newMap[cell[0]] = function

        return newMap

    def determineAction(self, neighbourList, centerState):
        if centerState < self.nStates:
            if self.decisionTreeUsed:
                return self.determineActionAux(neighbourList, 0, self.decisionTree[centerState])
            else:
                nNeighbours = [0] * (self.nStates - 1)
                for neighbour in neighbourList:
                    if neighbour > 0:
                        nNeighbours[neighbour - 1] = nNeighbours[neighbour - 1] + 1

                i = 0
                position = self.neighbourTree[centerState]
                while i < self.nStates - 1:
                    if i == self.nStates - 2:
                        return position[nNeighbours[i]]
                    else:
                        position = position[nNeighbours[i]]
                    i = i + 1
        else:
            return centerState

    def determineActionAux(self, neighbourList, i, decisionTree):
        if i < len(neighbourList):
            return self.determineActionAux(neighbourList, i + 1, decisionTree[neighbourList[i]])
        else:
            return decisionTree

    def findNeighbourList(self, coords, map):
        mapSegment = self.findNeighbourListAux(coords, 0, map, [])
        return mapSegment

    def findNeighbourListAux(self, coords, i, map, localcoords):
        if isinstance(map, int):
            if self.useCenter or localcoords != self.center:
                if self.moorelian:
                    return map
                else:
                    if self.findNeumannDistance(localcoords):
                        return map
                    else:
                        return None
        else:
            lowerbound = coords[i] - self.center[i]
            upperbound = coords[i] - self.center[i] + self.neighbourhoodLength
            mapSegment = []
            for j in range(lowerbound, upperbound):
                value = self.findNeighbourListAux(coords, i + 1, map[j], localcoords + [j - coords[i] + self.center[i]])
                if value is not None:
                    mapSegment.append(value)
            return mapSegment


if __name__ == '__main__':
    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthFunction(state):
        return 1
    TestRule = Rule(True, 3, 2, [1, 1], False, dieFunction)
    TestRule.addRule([2], stayFunction)
    TestRule.addRule([3], birthFunction)
    print(TestRule.neighbourTree)