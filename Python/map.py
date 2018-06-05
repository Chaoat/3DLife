from sharedMemory import SharedState
import sys


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
        self.outerState = outerState
        self.map = self.createMap(dimensions, 0)

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
        sys.stdout.flush()
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
        for i in range(0, len(selfInfo[0])):
            cell = selfInfo[0][i]
            map = map + str(cell)
            if i + 1 < len(selfInfo[0]):
                map = map + ','
        
        dimensions = ''
        for i in range(0, len(selfInfo[1])):
            dimension = selfInfo[1][i]
            dimensions = dimensions + str(dimension)
            if i + 1 < len(selfInfo[1]):
                dimensions = dimensions + ','

        writeFile = open(directory, 'w')
        writeFile.write(map + '\n')
        writeFile.write(dimensions + '\n')
        writeFile.write(str(self.outerState) + '\n')
        wrapString = ''
        for i in range(0, len(self.wrap)):
            wrap = self.wrap[i]
            if wrap:
                wrapString = wrapString + '1'
            else:
                wrapString = wrapString + '0'
            if i + 1 < len(self.wrap):
                wrapString = wrapString + ','
        writeFile.write(wrapString)

if __name__ == '__main__':
    # TestMap = Map([10, 10], [True, True], 0)
    # TestMap[1][0] = 1
    # TestMap[0][1] = 1
    # TestMap[0][0] = 1

    testArray = [[]]
    testArray.append(WrapList(10, True, 0))
    print(testArray)