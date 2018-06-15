import sys
import time


from BorderLayout import BorderLayout as Bl
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QFileDialog,QLabel,
                             QMainWindow, QAction, qApp, QHBoxLayout, QGridLayout, QInputDialog, QComboBox,
                             QVBoxLayout)

import map, rule, fileSystem, tempus
from auxGUI import RuleUI, MapUI
from UIEvents import EventHandler


class GameOfLifeGUI(QMainWindow, EventHandler):
    def __init__(self):
        super().__init__()

        self.map = None
        self.rule = None
        self.speed = 10
        self.timeStates = 1

        self.time = None

        self.ruleUI = RuleUI(self)
        self.mapUI = MapUI(self)

        self.initUI()
        self._connectButtons()

    def initUI(self):

        self.importMapB = QPushButton('Import Map File')
        self.importRuleB = QPushButton('Import Rule File')
        self.speedB = QPushButton('Set Simulation Speed')
        self.pastStatesB = QPushButton('Set Number of Past States')

        self.mapNameL = QLabel("Map: None")
        self.ruleNameL = QLabel("Rule: None")
        self.simSpeedL = QLabel("Speed: 10 frame/sec")
        self.pastStatesL = QLabel("Past States: 1")

        self.generateB = QPushButton('Generate Simulation')

        self.currentSimL = QLabel("Current Simulation: None")

        self.createRuleB = QPushButton('Create new Rule')
        self.createMapB = QPushButton('Create new Map')

        self.goB = QPushButton('Start Simulation')
        self.goB.setCheckable(True)
        self.stepB = QPushButton('Step')

        self.drawModeB = QPushButton('Toggle draw mode')
        self.drawModeB.setCheckable(True)
        self.saveExportB = QPushButton('Export Current Map State')


        importBLayout = QVBoxLayout()
        importBLayout.addWidget(self.importMapB)
        importBLayout.addWidget(self.importRuleB)
        importBLayout.addWidget(self.speedB)
        importBLayout.addWidget(self.pastStatesB)

        labelLayout = QVBoxLayout()
        labelLayout.addWidget(self.mapNameL)
        labelLayout.addWidget(self.ruleNameL)
        labelLayout.addWidget(self.simSpeedL)
        labelLayout.addWidget(self.pastStatesL)

        topLayout = QHBoxLayout()
        topLayout.addLayout(importBLayout)
        topLayout.addLayout(labelLayout)

        goLayout = QHBoxLayout()
        goLayout.addWidget(self.goB)
        goLayout.addWidget(self.stepB)

        quitButton = QPushButton('Exit')
        quitButton.clicked.connect(QApplication.instance().quit)

        mapLayout = QHBoxLayout()
        mapLayout.addWidget(self.drawModeB)
        mapLayout.addWidget(self.saveExportB)

        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addWidget(self.generateB)
        layout.addWidget(self.currentSimL)
        layout.addWidget(self.createRuleB)
        layout.addWidget(self.createMapB)
        layout.addStretch(1)
        layout.addLayout(goLayout)
        layout.addLayout(mapLayout)
        layout.addWidget(quitButton)

        mainWindow = QWidget()
        mainWindow.setLayout(layout)
        self.setCentralWidget(mainWindow)


        #SHOW WIDGET
        self.setGeometry(300, 300, 900, 660)
        self.centerWindow()
        self.setWindowTitle('The Game of Life')
        self.setWindowIcon(QIcon('pillow.jpg'))
        self.show()



    def _connectButtons(self):
        self.importMapB.clicked.connect(self.importMap)
        self.importRuleB.clicked.connect(self.importRule)
        self.speedB.clicked.connect(self.setSpeed)
        self.pastStatesB.clicked.connect(self.setTimeStates)

        self.createRuleB.clicked.connect(self.createRule)

        self.createMapB.clicked.connect(self.createMap)

        self.generateB.clicked.connect(self.generateSimulation)

        self.goB.clicked[bool].connect(self.startStopThread)
        self.stepB.clicked.connect(self.step)
        self.drawModeB.clicked[bool].connect(self.toggleDrawMode)
        self.saveExportB.clicked.connect(self.exportMap)


    #ESCAPE EXIT
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.close()

    #CENTERING WINDOW ON SCREEN
    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())




if __name__ == '__main__':
    app = QApplication(sys.argv)    #create application


    ex = GameOfLifeGUI()

    sys.exit(app.exec_())           #execute application, exit when finished