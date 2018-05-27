import map
import rule

def GliderTest():
    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthFunction(state):
        return 1
    TestRule = rule.Rule(True, 3, 2, [1, 1], True, dieFunction)
    TestRule.addRule([2], stayFunction)
    TestRule.addRule([3], birthFunction)

    TestMap = map.Map([40, 40], [True, True], 0)
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
    TestMap = map.Map([10, 10, 10], [True, True, True], 0)
    TestMap[2][1][4] = 1
    TestMap[3][2][4] = 1
    TestMap[4][2][4] = 1
    TestMap[2][3][4] = 1
    TestMap[3][3][4] = 1
    TestMap[2][1][5] = 1
    TestMap[3][2][5] = 1
    TestMap[4][2][5] = 1
    TestMap[2][3][5] = 1
    TestMap[3][3][5] = 1
    TestMap.print3D()

    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthStayFunction(state):
        return 1
    TestRule = rule.Rule(True, 3, 2, [1, 1, 1], False, dieFunction)
    TestRule.addRule([5], stayFunction)
    TestRule.addRule([6], birthStayFunction)
    TestRule.addRule([7], stayFunction)

    while True:
        input('')
        TestMap = TestRule.processMap(TestMap)
        TestMap.print3D()

if __name__ == '__main__':
    ThreeDTest()