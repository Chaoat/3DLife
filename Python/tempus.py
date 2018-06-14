import time
import map
from sharedMemory import SharedState

class Time:
    def __init__(self, initialMap, rules, frequency=10, timeStatesToDisplay=1):
        self.rules = []
        self.nTimeDimensions = 0
        self.turnN = 0
        self.lastFrameTime = time.time()
        self.frequency = frequency
        self.running = False
        self.drawMode = False
        self.timeStatesToDisplay = timeStatesToDisplay

        try:
            for rule in rules:
                self.rules.append(rule)
                self.nTimeDimensions = self.nTimeDimensions + 1
        except TypeError:
            self.rules.append(rules)
            self.nTimeDimensions = 1

        self.spaceDimensions = initialMap.dimensions
        self.maps = [initialMap]
        currentmap = self.maps
        for i in range(0, self.nTimeDimensions - 1):
            currentmap[0] = [initialMap]
            currentmap = currentmap[0]

        # create shared memory for C++ integration
        self.sharedState = SharedState(self.spaceDimensions, timeStatesToDisplay)

    def setDrawMode(self, mode:bool):
        self.sharedState.setDrawMode(mode)

    def changeFrequency(self, frequency):
        self.frequency = frequency

    def update(self, properties={}):
        currentTime = time.time()
        dt = currentTime - self.lastFrameTime
        self.drawMode = self.sharedState.getData().drawMode
        if self.running:
            if self.drawMode:
                print("pausing", self.turnN)
                self.pause()
            elif dt > 1/self.frequency:
                print("step", self.turnN)
                self.step(properties)
        elif self.drawMode:
            passmaps = [self.getEmptyMap() for _ in range(self.timeStatesToDisplay)]
            print("reading", self.turnN, "dims", [len(passmaps)] + passmaps[0].dimensions)
            self.maps = self.sharedState.get3DMaps(passmaps)
        else:
            print("resuming", self.turnN)
            self.run()


    def step(self, properties={}):
        self.lastFrameTime = time.time()
        self.processTurn()
        maps = self.getMaps()
        
        passmaps = []
        for i in range(0, self.timeStatesToDisplay):
            index = self.turnN - self.timeStatesToDisplay + i + 1
            if index > 0:
                passmaps.append(maps[index].map)
            else:
                passmaps.append(self.getEmptyMap().map)

        # write maps to shared mem
        self.sharedState.setMaps(passmaps)

        # print(self.timeStatesToDisplay)
        if 'draw' in properties:
            if len(self.spaceDimensions) == 1:
                maps[self.turnN].print1D()
            elif len(self.spaceDimensions) == 2:
                maps[self.turnN].print2D()
            elif len(self.spaceDimensions) == 3:
                maps[self.turnN].print3D()

    def getEmptyMap(self):
        return map.Map(self.spaceDimensions, self.maps[0].wrap, 0)

    def run(self):
        self.running = True

    def pause(self):
        self.running = False

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