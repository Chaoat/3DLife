import os
import operator
from functools import reduce

class WrapList:
    def __init__(self, length, wrap, outerState):
        self.length = length
        self.list = [None]*length
        self.wrap = wrap
        self.outerState = outerState

    def __len__(self):
        return self.length

    def __iter__(self):
        return WrapListIterator(self.list)

    def __getitem__(self, index):
        if self.wrap:
            index = index%self.length
        else:
            if index < 0 or index >= self.length:
                return self.outerState
        return self.list[index]

    def __setitem__(self, index, value):
        index = index%self.length
        self.list[index] = value

    def __str__(self):
        string = '['
        for i in range(0, len(self.list)):
            string = string + str(self.list[i])
            if i < len(self.list) - 1:
                string = string + ', '
        string = string + ']'
        return string

class WrapListIterator:
    def __init__(self, list):
        self.list = list
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < len(self.list):
            item = self.list[self.i]
            self.i = self.i + 1
            return item
        else:
            raise StopIteration()

class Map:
    def __init__(self, dimensions, wrap, outerState):
        self.dimensions = dimensions
        self.wrap = wrap
        self.nDimensions = len(dimensions)
        self.outerState = outerState
        self.map = self.createMap(dimensions, 0)

        self.cellsPerDimension = [1]
        for i in range(0, len(self.dimensions)):
            self.cellsPerDimension.append(self.cellsPerDimension[i] * self.dimensions[i])

        self.oneDIndices = [[] for _ in range(self.cellsPerDimension[-1])]

        for d in range(len(self.dimensions)):
            for c in range(self.cellsPerDimension[-1]):
                self.oneDIndices[c].append(c // self.cellsPerDimension[d] % self.cellsPerDimension[d + 1]) 

    def duplicateMap(self):
        NewMap = Map(self.dimensions, self.wrap, self.outerState)
        cells = self.findAllCells()
        for cell in cells:
            NewMap[cell[0]] = cell[1]
        return NewMap

    def findAllCells(self):
        return self.findAllCellsAux(self.map)

    def findAllCellsAux(self, map):
        elements = []
        for i in range(0, len(map)):
            if isinstance(map[i], int):
                elements.append([[i], map[i]])
            else:
                childElements = self.findAllCellsAux(map[i])
                for element in childElements:
                    elements.append([[i] + element[0], element[1]])
        return elements

    def createMap(self, dimensions, i):
        if len(dimensions) > i:
            outerState = self.outerState
            if not self.wrap[i]:
                outerState = self.defineOuterRegion(dimensions[i + 1:])
            map = WrapList(dimensions[i], self.wrap[i], outerState)

            for j in range(0, dimensions[i]):
                map[j] = self.createMap(dimensions, i + 1)
            return map
        else:
            return 0

    def defineOuterRegion(self, dimensions):
        if len(dimensions) > 0:
            wrapArray = []
            for i in range(0, dimensions[0]):
                wrapArray.append(False)
            returnArray = WrapList(dimensions[0], wrapArray, None)
            for i in range(0, dimensions[0]):
                returnArray[i] = self.defineOuterRegion(dimensions[1:])
            return returnArray
        else:
            return self.outerState

    def __getitem__(self, index):
        if isinstance(index, int) or isinstance(index, slice):
            return self.map[index]
        else:
            element = self.map
            while len(index) > 0:
                element = element[index[0]]
                index = index[1:]
            return element

    def __setitem__(self, index, value):
        if isinstance(index, int):
            self[index] = value
        else:
            element = self.map
            while len(index) > 1:
                element = element[index[0]]
                index = index[1:]
            element[index[0]] = value

    def __str__(self):
        return str(self.map)

    def getDimensions(self):
        return self.dimensions

    def __iter__(self):
        return WrapListIterator(self.map)

    def print2D(self):
        os.system('cls')
        text = ''
        for i in range(0, self.dimensions[1]):
            text = text + '\n'
            for j in range(0, self.dimensions[0]):
                text = text + str(self.map[j][i])
        print(text)

    def print3D(self):
        for i in range(0, self.dimensions[1]):
            line = ''
            for j in range(0, self.dimensions[2]):
                for k in range(0, self.dimensions[0]):
                    line = line + str(self.map[k][i][j])
                line = line + ' '
            print(line)

    def exportInfo(self):
        mapArray = self.iterateMap(self.map)
        return [mapArray, self.dimensions]

    def exportOneDInfo(self):
        ret = [0 for _ in range(self.cellsPerDimension[-1])]

        # prints the array of indices
        # for i in range(cellsPerDimension[-1]):
        #     print(arr[i], end=" ")
        #     if i % self.dimensions[0] == self.dimensions[0] - 1:
        #         print()

        for c in range(self.cellsPerDimension[-1]):
            ret[c] = reduce(operator.getitem, self.oneDIndices[c], self.map)
        
        return ret

    def iterateMap(self, map):
        if isinstance(map, WrapList):
            mapArray = []
            for dimension in map:
                mapArray = mapArray + self.iterateMap(dimension)
            return mapArray
        else:
            return [map]

    def saveMap(self, directory):
        selfInfo = self.exportInfo()
        map = ''
        for cell in selfInfo[0]:
            map = map + str(cell) + ','
        dimensions = ''
        for dimension in selfInfo[1]:
            dimensions = dimensions + str(dimension) + ','

        writeFile = open(directory, 'w')
        writeFile.write(map + '\n')
        writeFile.write(dimensions + '\n')
        writeFile.write(str(self.outerState) + '\n')
        wrapString = ''
        for wrap in self.wrap:
            if wrap:
                wrapString = wrapString + '1,'
            else:
                wrapString = wrapString + '0,'
        writeFile.write(wrapString)

if __name__ == '__main__':
    TestMap = Map([10, 10], [True, True], 0)
    TestMap[1][0] = 1
    TestMap[0][1] = 1
    TestMap[0][0] = 1

    print(TestMap.exportOneDInfo())
