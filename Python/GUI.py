import sys
import time


from BorderLayout import BorderLayout as Bl
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QFileDialog,QLabel,
                             QMainWindow, QAction, qApp, QHBoxLayout, QGridLayout, QInputDialog, QComboBox)

import map, rule, fileSystem, tempus
from auxGUI import SimButtons, RuleUI
from UIEvents import EventHandler


class GameOfLifeGUI(QMainWindow, EventHandler):
    def __init__(self):
        super().__init__()

        # self.eh = eventHandler.eventHandler()

        self.map = None
        self.rule = None
        self.time = None

        self.mapName = QLabel('Please import a map')
        self.ruleName = QLabel('Please import a rule')

        self.run = None
        self.speed = 1


        self.ruleUI = RuleUI()

        self.initUI()

    def initUI(self):

        #Buttons
        self.simButtons = SimButtons()

        self._connectButtons()

        self.gameInfo = QWidget()
        gameInfoLayout = QGridLayout()
        gameInfoLayout.addWidget(self.mapName,  *(0, 0))
        gameInfoLayout.addWidget(self.ruleName, *(1, 0))
        self.gameInfo.setLayout(gameInfoLayout)

        #SetLayout
        layout = Bl()

        layout.addWidget(self.simButtons,   Bl.Center)
        layout.addWidget(self.gameInfo,     Bl.East)


        mainWindow = QWidget()
        mainWindow.setLayout(layout)
        self.setCentralWidget(mainWindow)



        #FILE MENU
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        importAct = QAction('&Import', self)
        importAct.setShortcut('Ctrl+I')
        importAct.setStatusTip('Import map')
        importAct.triggered.connect(self.importMap)
        exportAct = QAction('&Export', self)
        exportAct.setShortcut('Ctrl+E')
        exportAct.setStatusTip('Export map')
        # exportAct.triggered.connect(self.exportMap)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(importAct)
        fileMenu.addAction(exportAct)
        fileMenu.addAction(exitAct)



        #SHOW WIDGET
        self.setGeometry(300, 300, 900, 660)
        self.center()
        self.setWindowTitle('The Game of Life')
        self.setWindowIcon(QIcon('pillow.jpg'))
        self.show()



    def _connectButtons(self):
        self.simButtons.goB.clicked.connect(self.go)
        self.simButtons.constructB.clicked.connect(self.constructGame)
        self.simButtons.stepOneB.clicked.connect(self.stepForward)
        self.simButtons.importMapB.clicked.connect(self.importMap)
        self.simButtons.importRuleB.clicked.connect(self.importRule)
        self.simButtons.stepTenB.clicked.connect(self.stepForwardTen)
        self.simButtons.pauseB.clicked.connect(self.pause)
        self.simButtons.createRuleB.clicked.connect(self.createMap)
        self.simButtons.drawModeB.clicked[bool].connect(self.toggleDrawMode)


    #Construct the layout and buttons for the main window
    def constructMainWindow(self):
        layout = Bl()

        #CAMERA CONTROLS: EAST 1 ##########################
        # controlLayout = QGridLayout()
        #
        # orbUp = QPushButton('up')               #Orbit
        # orbLeft = QPushButton('left')
        # orbit = QPushButton('ORBIT')
        # orbRight = QPushButton('right')
        # orbDown = QPushButton('down')
        #
        # orbUp.setAccessibleName('up')
        # orbLeft.setAccessibleName('left')
        # orbRight.setAccessibleName('right')
        # orbDown.setAccessibleName('down')
        #
        # orbUp.clicked.connect(self.orbitCamera)
        # orbLeft.clicked.connect(self.orbitCamera)
        # orbRight.clicked.connect(self.orbitCamera)
        # orbDown.clicked.connect(self.orbitCamera)
        #
        # moveUp = QPushButton('up')              #Movement
        # moveLeft = QPushButton('left')
        # move = QPushButton('MOVE')
        # moveRight = QPushButton('right')
        # moveDown = QPushButton('down')
        #
        # moveUp.setAccessibleName('up')
        # moveLeft.setAccessibleName('left')
        # moveRight.setAccessibleName('right')
        # moveDown.setAccessibleName('down')
        #
        # moveUp.clicked.connect(self.moveCamera)
        # moveLeft.clicked.connect(self.moveCamera)
        # moveRight.clicked.connect(self.moveCamera)
        # moveDown.clicked.connect(self.moveCamera)
        #
        # zoomIn = QPushButton('zoom in')             #zoom
        # zoomOut = QPushButton('zoom out')
        #
        # zoomIn.setAccessibleName('zoomIn')
        # zoomOut.setAccessibleName('zoomOut')
        #
        # zoomIn.clicked.connect(self.zoomCamera)
        # zoomOut.clicked.connect(self.zoomCamera)
        #
        # camReset = QPushButton('reset camera')      #reset
        # camReset.clicked.connect(self.resetCamera)
        #
        # controlLayout.addWidget(orbUp,      *(0, 1))
        # controlLayout.addWidget(orbLeft,    *(1, 0))
        # controlLayout.addWidget(orbit,      *(1, 1))
        # controlLayout.addWidget(orbRight,   *(1, 2))
        # controlLayout.addWidget(orbDown,    *(2, 1))
        #
        # controlLayout.addWidget(moveUp,     *(3, 1))
        # controlLayout.addWidget(moveLeft,   *(4, 0))
        # controlLayout.addWidget(move,       *(4, 1))
        # controlLayout.addWidget(moveRight,  *(4, 2))
        # controlLayout.addWidget(moveDown,   *(5, 1))
        #
        # controlLayout.addWidget(zoomIn,     *(6, 0))
        # controlLayout.addWidget(zoomOut,    *(6, 1))
        # controlLayout.addWidget(camReset,   *(6, 2))
        #
        # controlWidget = QWidget()
        # controlWidget.setLayout(controlLayout)
        # layout.addWidget(controlWidget, Bl.West)


        #DRAW MODE: SOUTH #############################################
        # drawLayout = QHBoxLayout()
        #
        # dm = QPushButton('Draw mode')                   #toggle drawmode
        # dm.setCheckable(True)
        # dm.clicked[bool].connect(self.toggleDrawMode)
        #
        # incDL = QPushButton('Increment draw layer')     #increment drawlayer
        # incDL.clicked.connect(self.incrementDrawLayer)
        #
        # decDL = QPushButton('Decrement draw layer')     #decrement drawlayer
        # decDL.clicked.connect(self.decrementDrawLayer)
        #
        # drawLayout.addWidget(dm)
        # drawLayout.addWidget(incDL)
        # drawLayout.addWidget(decDL)
        # # drawLayout.stretch(1)
        #
        # drawWidget = QWidget()
        # drawWidget.setLayout(drawLayout)
        # layout.addWidget(drawWidget, Bl.South)


        #SIMULATION CONTROLS ######################################

        # dimBox = QComboBox(self)
        # dimBox.addItem('Set Dimensions')
        # for i in range(2,6):
        #     dimBox.addItem(str(i))
        # dimBox.activated[str].connect(changeDimension)



        self.mapName = QLabel("Please import a map")
        self.ruleName = QLabel("Please import a rule")

        return mainWindow



    def setSpeed(self):
        i, okPressed = QInputDialog.getInt(self, "Enter ticks per second", "Speed:", 0, 0, 100, 1)
        if okPressed:
            self.speed = i





    #Reset rules
    def resetRules(self):
        self.rule = rule.Rule(True, 3, 2, [1, 1, 1], False, self.dieFunction)
        self.ruleList = []
        print(self.ruleList)

    #Add Rule Event
    def addRule(self):
        items = ("Die", "Stay", "Birth")
        item, okPressed = QInputDialog.getItem(self, "Choose Rule", "Rule:", items, 0, False)
        if okPressed and item:
            self._addRule(item)
            print(self.ruleList)

    def _addRule(self, rule):
        i, okPressed = QInputDialog.getInt(self, "Adjacent Living Cells", "Number:", 1, 0, 100, 1)
        if okPressed:
            if rule == "Die":
                self.rule.addRule([i], self.dieFunction)
                self.ruleList.append('Dies with ' + str(i) + ' adjacent living cells')
            elif rule == "Stay":
                self.rule.addRule([i], self.stayFunction)
                self.ruleList.append('Remains with ' + str(i) + ' adjacent living cells')
            elif rule == "Birth":
                self.rule.addRule([i], self.birthFunction)
                self.ruleList.append('Births with ' + str(i) + ' adjacent living cells')
            print(self.ruleList)

    #Change dimension event
    #Events for camera movement
    def orbitCamera(self):
        source = self.sender()

        if source.accessibleName() == 'up':
            self.statusBar().showMessage('orbit up')
        elif source.accessibleName() == 'left':
            self.statusBar().showMessage('orbit left')
        elif source.accessibleName() == 'right':
            self.statusBar().showMessage('orbit right')
        elif source.accessibleName() == 'down':
            self.statusBar().showMessage('orbit down')
    def moveCamera(self):
        source = self.sender()

        if source.accessibleName() == 'up':
            self.statusBar().showMessage('move up')
        elif source.accessibleName() == 'left':
            self.statusBar().showMessage('move left')
        elif source.accessibleName() == 'right':
            self.statusBar().showMessage('move right')
        elif source.accessibleName() == 'down':
            self.statusBar().showMessage('move down')
    def zoomCamera(self):
        source = self.sender()

        if source.accessibleName() == 'zoomIn':
            self.statusBar().showMessage('zoom in')
        elif source.accessibleName() == 'zoomOut':
            self.statusBar().showMessage('zoom out')
    def resetCamera(self):
        self.statusBar().showMessage('reset camera')

    #Events for draw mode
    def toggleDrawMode(self, pressed):
        if pressed:
            self.statusBar().showMessage('draw mode ON')
        else:
            self.statusBar().showMessage('draw mode OFF')
    def incrementDrawLayer(self):
        self.statusBar().showMessage('increment draw layer')
    def decrementDrawLayer(self):
        self.statusBar().showMessage('decrement draw layer')



    #ESCAPE EXIT
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.close()
    #CENTERING WINDOW ON SCREEN
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())





if __name__ == '__main__':
    app = QApplication(sys.argv)    #create application


    ex = GameOfLifeGUI()

    sys.exit(app.exec_())           #execute application, exit when finished