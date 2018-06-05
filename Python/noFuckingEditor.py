import map

def gliderTest():
    saveMap = map.Map([12, 10], [True, True], 0)
    saveMap[2][1] = 1
    saveMap[3][2] = 1
    saveMap[1][3] = 1
    saveMap[2][3] = 1
    saveMap[3][3] = 1
    saveMap.saveMap('Maps/Conways/gliderTest.map')

def wireworldTest1():
    saveMap = map.Map([12, 10], [True, True], 0)
    saveMap[3][3] = 1
    saveMap[4][3] = 3
    saveMap[5][3] = 3
    saveMap[6][3] = 3
    saveMap[7][3] = 3
    saveMap[8][3] = 3
    saveMap[9][3] = 3
    saveMap[10][4] = 3
    saveMap[10][5] = 3
    saveMap[3][6] = 3
    saveMap[4][6] = 3
    saveMap[5][6] = 3
    saveMap[8][6] = 3
    saveMap[6][7] = 3
    saveMap[6][5] = 3
    saveMap[7][7] = 3
    saveMap[7][6] = 3
    saveMap[7][5] = 3
    saveMap[9][6] = 3
    saveMap[2][4] = 3
    saveMap[2][5] = 3
    saveMap.saveMap('Maps/Wireworld/wireworld1.map')

def LargerThanLife1Butterfly():
    saveMap = map.Map([70, 50], [True, True], 0)
    saveMap[30][22] = 1
    saveMap[32][22] = 1
    saveMap[29][23] = 1
    saveMap[30][23] = 1
    saveMap[31][23] = 1
    saveMap[32][23] = 1
    saveMap[29][24] = 1
    saveMap[30][24] = 1
    saveMap[31][24] = 1
    saveMap[32][24] = 1
    saveMap[33][24] = 1
    saveMap[29][25] = 1
    saveMap[30][25] = 1
    saveMap[31][25] = 1
    saveMap[32][25] = 1
    saveMap[33][25] = 1
    saveMap[29][26] = 1
    saveMap[30][26] = 1
    saveMap[31][26] = 1
    saveMap[32][26] = 1
    saveMap[33][26] = 1
    saveMap[29][27] = 1
    saveMap[30][27] = 1
    saveMap[31][27] = 1
    saveMap[32][27] = 1
    saveMap[33][27] = 1
    saveMap[29][28] = 1
    saveMap[30][28] = 1
    saveMap[31][28] = 1
    saveMap[32][28] = 1
    saveMap[33][28] = 1
    saveMap[29][29] = 1
    saveMap[30][29] = 1
    saveMap[31][29] = 1
    saveMap[32][29] = 1
    saveMap[30][30] = 1
    saveMap[32][30] = 1
    saveMap.saveMap('Maps/LargerThanLife1/butterfly.map')

def TestIndexMap():
    saveMap = map.Map([3, 3, 3, 3], [True, True, True, True], 0)
    for i in range(0, 3):
        for j in range(0, 3):
            for k in range(0, 3):
                for m in range(0, 3):
                    saveMap[i][j][k][m] = str(i) + str(j) + str(k) + str(m)
    saveMap.saveMap('Maps/testIndexMap.map')

def ThreeDTestMap():
    saveMap = map.Map([10, 10, 10], [True, True, True], 0)

    saveMap[5][5][5] = 1
    saveMap[6][5][5] = 1

    saveMap[7][4][5] = 1
    saveMap[7][3][5] = 1

    saveMap[4][4][5] = 1
    saveMap[4][3][5] = 1

    saveMap[5][4][6] = 1
    saveMap[5][3][6] = 1
    saveMap[6][4][6] = 1
    saveMap[6][3][6] = 1

    saveMap.saveMap('Maps/3dLife/threeDTestMap.map')

if __name__ == '__main__':
    ThreeDTestMap()