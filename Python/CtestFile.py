import map
import rule
import Time

def exportMap():
    info = TestTime.getLatestMapFirstD()
    return info[0]

def exportDimensions():
    info = TestTime.getLatestMapFirstD()
    return info[1]

def dieFunction(state):
    return 0

def stayFunction(state):
    return state

def birthFunction(state):
    return 1

TestRule = rule.Rule(True, 3, 2, [1, 1], True, dieFunction)

TestRule = rule.Rule(True, 3, 2, [1, 1], True, dieFunction)
TestRule.addRule([2], stayFunction)
TestRule.addRule([3], birthFunction)

TestMap = map.Map([40, 40], [True, True], 0)
TestMap[2][1] = 1
TestMap[3][2] = 1
TestMap[4][2] = 1
TestMap[2][3] = 1
TestMap[3][3] = 1

TestTime = Time.Time(TestMap, TestRule)
while True:
    TestTime.update({})