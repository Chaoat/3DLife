import map
import rule

if __name__ == '__main__':
    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthFunction(state):
        return 1
    TestRule = rule.Rule(True, 3, 2, [1, 1], dieFunction)
    TestRule.addRule([2], stayFunction)
    TestRule.addRule([3], birthFunction)

    TestMap = map.Map([10, 10], [True, True], 0)
    TestMap[1][1] = 1
    TestMap[2][2] = 1
    TestMap[3][2] = 1
    TestMap[1][3] = 1
    TestMap[2][3] = 1
    TestMap.print2D()
    while True:
        print('gap')
        TestMap = TestRule.processMap(TestMap)
        TestMap.print2D()
