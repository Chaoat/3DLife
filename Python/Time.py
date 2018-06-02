import time

class Time:
    def __init__(self, innitialMap, rules):
        self.rules = []
        self.nTimeDimensions = 0
        self.turnN = 0
        self.lastFrameTime = time.time()
        self.frequency = 10

        try:
            for rule in rules:
                self.rules.append(rule)
                self.nTimeDimensions = self.nTimeDimensions + 1
        except TypeError:
            self.rules.append(rules)
            self.nTimeDimensions = 1

        self.spaceDimensions = innitialMap.dimensions
        self.maps = [innitialMap]
        currentmap = self.maps
        for i in range(0, self.nTimeDimensions - 1):
            currentmap[0] = [innitialMap]
            currentmap = currentmap[0]

    def update(self, properties={}):
        currentTime = time.time()
        dt = currentTime - self.lastFrameTime
        if dt > 1/self.frequency:
            self.step(properties)

    def step(self, properties={}):
        self.lastFrameTime = time.time()
        self.processTurn()

        if 'draw' in properties:
            latestMap = self.getMaps()[self.turnN]
            latestMap.print2D()

    def processTurn(self):
        self.processTurnAux(self.maps, 0, 0)
        self.turnN = self.turnN + 1

    def processTurnAux(self, map, rulei, depth):
        if depth < self.nTimeDimensions:
            lastMap = map[len(map) - 1]
            map.append(self.rules[rulei].processMap(lastMap))
            for nextmap in map:
                self.processTurnAux(nextmap, rulei + 1, depth + 1)

    def getMaps(self):
        return self.maps

    def getTurnN(self):
        return self.turnN

    def exportInfo(self):
        timeArray = self.iterateTime(self.maps)
        return [timeArray, self.turnN]

    def getLatestMapFirstD(self):
        return self.maps[self.turnN].exportInfo()

    def iterateTime(self, time):
        if isinstance(time, list):
            timeArray = []
            for dimension in time:
                timeArray = timeArray + self.iterateTime(dimension)
            return timeArray
        else:
            return time.exportInfo()