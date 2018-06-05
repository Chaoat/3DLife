import PyQt5
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget,
                             QMainWindow, QAction, qApp, QMenu, QTextEdit, QLabel, QHBoxLayout, QVBoxLayout,
                             QGridLayout, QLCDNumber, QSlider, QLineEdit, QInputDialog, QFrame, QColorDialog,
                             QSizePolicy, QFontDialog, QFileDialog, QCheckBox, QProgressBar, QCalendarWidget,
                             QSplitter, QComboBox)
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap, QDrag, QPicture
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QBasicTimer, QDate, QMimeData
from BorderLayout import BorderLayout as Bl


#ACCESS ANDREW'S FILES
from Python import map, fileSystem, rule
import time




class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()

        self.map = map.Map([10, 10, 10], [True, True, True], 0)

        def dieFunction(state):
            return 0
        self.rule = rule.Rule(True, 3, 2, [1, 1, 1], False, dieFunction)
        self.ruleList = []

        self.on = False
        self.speed = 1

        self.initUI()

    def initUI(self):



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
        exportAct.triggered.connect(self.exportMap)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(importAct)
        fileMenu.addAction(exportAct)
        fileMenu.addAction(exitAct)


        #CREATE MAIN WINDOW
        mainWindow = self.constructMainWindow()
        self.setCentralWidget(mainWindow)


        #SHOW WIDGET
        self.setGeometry(300, 300, 1500, 1100)
        self.center()
        self.setWindowTitle('The Game of Life')
        self.setWindowIcon(QIcon('pillow.jpg'))
        self.show()



    #Construct the layout and buttons for the main window
    def constructMainWindow(self):
        layout = Bl()

        #CAMERA CONTROLS: EAST 1 ##########################
        controlLayout = QGridLayout()

        orbUp = QPushButton('up')               #Orbit
        orbLeft = QPushButton('left')
        orbit = QPushButton('ORBIT')
        orbRight = QPushButton('right')
        orbDown = QPushButton('down')

        orbUp.setAccessibleName('up')
        orbLeft.setAccessibleName('left')
        orbRight.setAccessibleName('right')
        orbDown.setAccessibleName('down')

        orbUp.clicked.connect(self.orbitCamera)
        orbLeft.clicked.connect(self.orbitCamera)
        orbRight.clicked.connect(self.orbitCamera)
        orbDown.clicked.connect(self.orbitCamera)

        moveUp = QPushButton('up')              #Movement
        moveLeft = QPushButton('left')
        move = QPushButton('MOVE')
        moveRight = QPushButton('right')
        moveDown = QPushButton('down')

        moveUp.setAccessibleName('up')
        moveLeft.setAccessibleName('left')
        moveRight.setAccessibleName('right')
        moveDown.setAccessibleName('down')

        moveUp.clicked.connect(self.moveCamera)
        moveLeft.clicked.connect(self.moveCamera)
        moveRight.clicked.connect(self.moveCamera)
        moveDown.clicked.connect(self.moveCamera)

        zoomIn = QPushButton('zoom in')             #zoom
        zoomOut = QPushButton('zoom out')

        zoomIn.setAccessibleName('zoomIn')
        zoomOut.setAccessibleName('zoomOut')

        zoomIn.clicked.connect(self.zoomCamera)
        zoomOut.clicked.connect(self.zoomCamera)

        camReset = QPushButton('reset camera')      #reset
        camReset.clicked.connect(self.resetCamera)

        controlLayout.addWidget(orbUp,      *(0, 1))
        controlLayout.addWidget(orbLeft,    *(1, 0))
        controlLayout.addWidget(orbit,      *(1, 1))
        controlLayout.addWidget(orbRight,   *(1, 2))
        controlLayout.addWidget(orbDown,    *(2, 1))

        controlLayout.addWidget(moveUp,     *(3, 1))
        controlLayout.addWidget(moveLeft,   *(4, 0))
        controlLayout.addWidget(move,       *(4, 1))
        controlLayout.addWidget(moveRight,  *(4, 2))
        controlLayout.addWidget(moveDown,   *(5, 1))

        controlLayout.addWidget(zoomIn,     *(6, 0))
        controlLayout.addWidget(zoomOut,    *(6, 1))
        controlLayout.addWidget(camReset,   *(6, 2))

        controlWidget = QWidget()
        controlWidget.setLayout(controlLayout)
        layout.addWidget(controlWidget, Bl.West)


        #DRAW MODE: SOUTH #############################################
        drawLayout = QHBoxLayout()

        dm = QPushButton('Draw mode')                   #toggle drawmode
        dm.setCheckable(True)
        dm.clicked[bool].connect(self.toggleDrawMode)

        incDL = QPushButton('Increment draw layer')     #increment drawlayer
        incDL.clicked.connect(self.incrementDrawLayer)

        decDL = QPushButton('Decrement draw layer')     #decrement drawlayer
        decDL.clicked.connect(self.decrementDrawLayer)

        drawLayout.addWidget(dm)
        drawLayout.addWidget(incDL)
        drawLayout.addWidget(decDL)
        # drawLayout.stretch(1)

        drawWidget = QWidget()
        drawWidget.setLayout(drawLayout)
        layout.addWidget(drawWidget, Bl.South)


        #SIMULATION CONTROLS ######################################
        simLayout = QGridLayout()

        dimBox = QComboBox(self)
        dimBox.addItem('Set Dimensions')
        for i in range(2,6):
            dimBox.addItem(str(i))
        dimBox.activated[str].connect(self.changeDimension)

        b1 = QPushButton('Go')
        b2 = QPushButton('Pause')
        b3 = QPushButton('Step')
        b4 = QPushButton('Set Speed')
        b5 = QPushButton('Add Rules')
        b6 = QPushButton('Reset Rules')

        b1.clicked.connect(self.go)
        b2.clicked.connect(self.pause)
        b3.clicked.connect(self.stepForward)
        b4.clicked.connect(self.setSpeed)
        b5.clicked.connect(self.chooseRule)
        b6.clicked.connect(self.resetRules)


        simLayout.addWidget(b1,     *(0, 0))
        simLayout.addWidget(b2,     *(0, 1))
        simLayout.addWidget(b3,     *(0, 2))
        simLayout.addWidget(b4,     *(1, 0))
        simLayout.addWidget(b5,     *(1, 1))
        simLayout.addWidget(b6,     *(1, 2))
        simLayout.addWidget(dimBox, *(2, 0))

        simWidget = QWidget()
        simWidget.setLayout(simLayout)
        layout.addWidget(simWidget, Bl.East)

        mainWindow = QWidget()
        mainWindow.setLayout(layout)

        return mainWindow

    def setRules(self):

        def dieFunction(state):
            return 0
        def stayFunction(state):
            return state
        def birthFunction(state):
            return 1

    def setSpeed(self):
        i, okPressed = QInputDialog.getInt(self, "Enter ticks per second", "Speed:", 0, 0, 100, 1)
        if okPressed:
            self.speed = i

    def pause(self):
        self.go = False

    def go(self):
        self.on = True
        while self.on:
            try:
                self.map = self.rule.processMap(self.map)
                self.map.print3D()
                time.sleep(1/self.speed)
            except KeyboardInterrupt:
                if not self.on:
                    break

    #Step Foward event
    def stepForward(self):
        if not self.on:
            self.map = self.rule.processMap(self.map)
            self.map.print3D()


    #Reset rules
    def resetRules(self):
        def dieFunction(state):
            return 0
        self.rule = rule.Rule(True, 3, 2, [1, 1, 1], False, dieFunction)
        self.ruleList = []

    #Add Rule Event
    def addRule(self):
        items = ("Die", "Stay", "Birth")
        item, okPressed = QInputDialog.getItem(self, "Choose Rule", "Rule:", items, 0, False)
        if okPressed and item:
            self._addRule(item)

    def _addRule(self, rule):
        i, okPressed = QInputDialog.getInt(self, "Adjacent Living Cells", "Number:", 0, 0, 100, 1)
        if okPressed:
            if rule == "Die":
                def dieFunction(state):
                    return 0
                self.rule.addRule([i], dieFunction)
                self.ruleList.append('Dies with ' + str(i) + ' adjacent living cells')
            elif rule == "Stay":
                def stayFunction(state):
                    return state
                self.rule.addRule([i], stayFunction)
                self.ruleList.append('Remains with ' + str(i) + ' adjacent living cells')
            elif rule == "Birth":
                def birthFunction(state):
                    return 1
                self.rule.addRule([i], birthFunction)
                self.ruleList.append('Births with ' + str(i) + ' adjacent living cells')


    #Change dimension event
    def changeDimension(self, text):
        if text != "Set dimensions":
            self.dimensions.setText(text)
            self.dimensions.adjustSize()


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

    #Import map
    def importMap(self):
        self.map
        return
    #Export map
    def exportMap(self):
        return


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


    ex = GameOfLife()

    sys.exit(app.exec_())           #execute application, exit when finished
