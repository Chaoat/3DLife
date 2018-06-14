import map
import rule
from tempus import Time
import fileSystem

import GUI
import sys
from PyQt5.QtWidgets import QApplication
import sys
import os

def GliderTest():
    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthFunction(state):
        return 1
        
    TestRule = rule.Rule(True, 3, 2, [1, 1], False, dieFunction)
    TestRule.addRule([2], stayFunction)
    TestRule.addRule([3], birthFunction)

    TestRule = fileSystem.loadRule(fileSystem.getProjectRoot() + 'Python/Rules/conways.rule')

    TestMap = map.Map([60, 60], [True, True], 0)
    TestMap[2][1] = 1
    TestMap[3][2] = 1
    TestMap[4][2] = 1
    TestMap[2][3] = 1
    TestMap[3][3] = 1
    TestMap.print2D()

    TestTime = Time(TestMap, TestRule)
    while True:
        TestTime.update({'draw': True})

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
    #TestMap.print3D()

    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthStayFunction(state):
        return 1
    def birthFunction(state):
        if state == 1:
            return 0
        else:
            return 1
    TestRule = rule.Rule(True, 3, 2, [1, 1, 1], False, dieFunction)
    TestRule.addRule([5], stayFunction)
    TestRule.addRule([6], birthStayFunction)
    TestRule.addRule([7], stayFunction)

    while True:
        input('')
        TestMap = TestRule.processMap(TestMap)
        # TestMap.print3D()

def TimeTest():
    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthFunction(state):
        return 1
    TestRule = rule.Rule(True, 3, 2, [1, 1], True, dieFunction)
    TestRule.addRule([2], stayFunction)
    TestRule.addRule([3], birthFunction)

    TestMap = map.Map([50, 30], [False, False], 1)
    TestMap[3][1] = 1
    TestMap[4][2] = 1
    TestMap[5][2] = 1
    TestMap[3][3] = 1
    TestMap[4][3] = 1
    TestMap.print2D()

    TestTime = Time(TestMap, TestRule)
    while True:
        TestTime.update({'draw':True})

def ExportTest():
    TestMap = map.Map([3, 4, 2], [False, False, False], 1)
    TestMap[0][0][0] = 111
    TestMap[0][1][0] = 121
    TestMap[0][2][0] = 131
    TestMap[0][3][0] = 141
    TestMap[1][0][0] = 211
    TestMap[1][1][0] = 221
    TestMap[1][2][0] = 231
    TestMap[1][3][0] = 241
    TestMap[2][0][0] = 311
    TestMap[2][1][0] = 321
    TestMap[2][2][0] = 331
    TestMap[2][3][0] = 341
    TestMap[0][0][1] = 112
    TestMap[0][1][1] = 122
    TestMap[0][2][1] = 132
    TestMap[0][3][1] = 142
    TestMap[1][0][1] = 212
    TestMap[1][1][1] = 222
    TestMap[1][2][1] = 232
    TestMap[1][3][1] = 242
    TestMap[2][0][1] = 312
    TestMap[2][1][1] = 322
    TestMap[2][2][1] = 332
    TestMap[2][3][1] = 342

    def dieFunction(state):
        return 0
    def stayFunction(state):
        return state
    def birthFunction(state):
        return 1
    TestRule = rule.Rule(True, 1, 2, [0, 0, 0], False, dieFunction)

    TestTime = Time(TestMap, TestRule)
    print(TestTime.exportInfo())
    TestTime.step()
    print(TestTime.exportInfo())

def Load2DTest(map, rule, frequency):
    TestMap = fileSystem.loadMap(map)
    TestMap.print2D()
    TestRule = fileSystem.loadRule(rule)
    TestTime = Time(TestMap, TestRule, frequency)

    while True:
        TestTime.update({'draw2D':True})

def DataTransferTest():
    # rule = input("""Select simulation:
    # 1. 1D - 1 Time Dimension
    # 2. 1D - 3 Time Dimensions
    # 3. 3D - 1 Time Dimension
    # 4. 3D - 3 Time Dimensions
    # """)
    # os.remove(fileSystem.getProjectRoot() + "tmp/3DLifeShmem")
    TestMap = None
    TestRule = None
    TestTime = None

    # andrew don't fuckin mess with this I swear you already have like 5 of your own test functions
    rule = sys.argv[1]
    if rule == "1":
        TestMap = fileSystem.loadMapRelative('1D/test1')
        TestRule = fileSystem.loadRuleRelative("1dlife")
        TestTime = Time(TestMap, TestRule, 8, 1)
    elif rule == "2":
        TestMap = fileSystem.loadMapRelative('1D/test1')
        TestRule = fileSystem.loadRuleRelative("1dlife")
        TestTime = Time(TestMap, TestRule, 1, 20)
    elif rule == "3":
        TestMap = fileSystem.loadMapRelative('3dLife/threeDTestMap')
        TestRule = fileSystem.loadRuleRelative("3dLife")
        TestTime = Time(TestMap, TestRule, 1, 1)
    elif rule == "4":
        TestMap = fileSystem.loadMapRelative('3dLife/threeDTestMap')
        TestRule = fileSystem.loadRuleRelative("3dLife")
        TestTime = Time(TestMap, TestRule, 1, 3)
    elif rule == "5":
        TestMap = fileSystem.loadMapRelative('Wireworld/wireworld1')
        TestRule = fileSystem.loadRuleRelative("wireworld")
        TestTime = Time(TestMap, TestRule, 8, 1)
    elif rule == "6":
        TestMap = fileSystem.loadMapRelative('Wireworld/4D')
        TestRule = fileSystem.loadRuleRelative("wireworld4d")
        TestTime = Time(TestMap, TestRule, 1, 1)
    elif rule == "7":
        TestMap = fileSystem.loadMapRelative('Conways/gliderTest')
        TestRule = fileSystem.loadRuleRelative("conways")
        TestTime = Time(TestMap, TestRule, 4, 1)
    elif rule == "8":
        TestMap = fileSystem.loadMapRelative('diagonal2d')
        TestRule = fileSystem.loadRuleRelative("wireworld")
        TestTime = Time(TestMap, TestRule, 10, 1)
    elif rule == "9":
        TestMap = fileSystem.loadMapRelative('diagonal2d')
        TestRule = fileSystem.loadRuleRelative("wireworld")
        TestTime = Time(TestMap, TestRule, 10, 1)
    
    TestTime.run()
    # for i in range(20):
    #     TestTime.step()

    # print("State of map:")
    # TestTime.sharedState.printData()
    while True:
        TestTime.update()

def Test(map, rule, frequency):
    TestMap = fileSystem.loadMapRelative(map)
    TestRule = fileSystem.loadRuleRelative(rule)
    TestTime = Time(TestMap, TestRule, frequency, 1)

    TestTime.run()
    while True:
        TestTime.update({'draw':True})

if __name__ == '__main__':
    # Load2DTest('Conways/gliderTest.map', 'conways', 10)
    # Load2DTest('Conways/gliderTest', 'conways', 10)

    Test('diagonal2d', 'wireworld', 10)
    #DataTransferTest()

    # app = QApplication(sys.argv)    #create application


    # ex = GUI.GameOfLifeGUI()

    # sys.exit(app.exec_())           #execute application, exit when finished
