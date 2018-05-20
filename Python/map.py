class Map:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.nDimensions = len(dimensions)
        self.map = []
        self.map = self.createMap(dimensions)

    def createMap(self, dimensions):
        if len(dimensions) > 0:
            map = [0]*dimensions[0]
            for i in range(0, dimensions[0]):
                map[i] = self.createMap(dimensions[1:])
            return map
        else:
            return 0

    def __getitem__(self, indices):
        try:
            return self.map[indices]
        except IndexError:
            return self.getitemaux(self.map, indices, 0)

    def getitemaux(self, map, indices, i):
        if len(indices) < i - 1:
            return self.getitemaux(map[i], indices, i + 1)
        else:
            return map[indices[i]]

    def __setitem__(self, indices, value):
        try:
            self.map[indices] = value
        except IndexError:
            self.setitemaux(self.map, indices, 0, value)

    def setitemaux(self, map, indices, i, value):
        if len(indices) < i - 1:
            self.setitemaux(map[i], indices, i + 1, value)
        else:
            map[indices[i]] = value

    def __str__(self):
        return str(self.map)

if __name__ == '__main__':
    TestMap = Map([2, 2, 2])
    TestMap[1][0][0] = 1
    TestMap[0][1][0] = 1
    TestMap[0][0][1] = 1
    print(TestMap)