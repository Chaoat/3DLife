import map
import rule

def GliderTest():
    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthFunction(state):
        return 1
    TestRule = rule.Rule(True, 3, 2, [1, 1], dieFunction)
    TestRule.addRule([2], stayFunction)
    TestRule.addRule([3], birthFunction)

    TestMap = map.Map([10, 20], [False, False], 1)
    TestMap[2][1] = 1
    TestMap[3][2] = 1
    TestMap[4][2] = 1
    TestMap[2][3] = 1
    TestMap[3][3] = 1
    TestMap.print2D()
    while True:
        input('')
        TestMap = TestRule.processMap(TestMap)
        TestMap.print2D()

def ThreeDTest():
    TestMap = map.Map([5, 5, 5], [True, True, True], 0)

    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthFunction(state):
        return 1
    TestRule = rule.Rule(True, 3, 3, [1, 1, 1], dieFunction)
    TestRule.addRule([2], stayFunction)
    TestRule.addRule([3], birthFunction)
    TestRule.addRule([4], birthFunction)

    while True:
        input('')
        TestMap = TestRule.processMap(TestMap)
        TestMap.print2D()

if __name__ == '__main__':
    GliderTest()