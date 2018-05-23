class WrapList:
    def __init__(self, length):
        self.length = length
        self.list = [None]*length

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        index = index%self.length
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
        self.map = []
        self.map = self.createMap(dimensions, 0)
        self.outerState = outerState

    def createMap(self, dimensions, i):
        if len(dimensions) > i:
            map = None
            if self.wrap[i]:
                map = WrapList(dimensions[0])
            else:
                map = [None]*dimensions[0]

            for j in range(0, dimensions[0]):
                map[j] = self.createMap(dimensions, i + 1)
            return map
        else:
            return 0

    def __getitem__(self, index):
        try:
            return self.map[index]
        except IndexError:
            return self.outerState

    def __str__(self):
        return str(self.map)

    def getDimensions(self):
        return self.dimensions

    def __iter__(self):
        return WrapListIterator(self.map)

if __name__ == '__main__':
    TestMap = Map([10, 10], [True, True], 0)
    TestMap[1][0] = 1
    TestMap[0][1] = 1
    TestMap[0][0] = 1
    print(TestMap)
    #print(TestMap[11][10])