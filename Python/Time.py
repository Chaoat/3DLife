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
                self.nTimeDimensions = self.ndimensions + 1
        except TypeError:
            self.rules.append(rules)
            self.nTimeDimensions = 1

        self.maps = [innitialMap]
        currentmap = self.maps
        for i in range(0, self.nTimeDimensions - 1):
            currentmap[0] = [innitialMap]
            currentmap = currentmap[0]

    def update(self, properties):
        currentTime = time.time()
        dt = currentTime - self.lastFrameTime
        if dt > 1/self.frequency:
            self.lastFrameTime = currentTime
            self.processTurn()

            if properties['draw']:
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

    def getMapString(self):
        mapArray = []
