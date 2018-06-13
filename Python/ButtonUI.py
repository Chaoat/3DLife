import sys
import time


from BorderLayout import BorderLayout as Bl
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QFileDialog,QLabel,
                             QMainWindow, QAction, qApp, QHBoxLayout, QGridLayout, QInputDialog, QComboBox,
                             QVBoxLayout)

import map, rule, fileSystem, tempus



class SimButtons(QWidget):

    def __init__(self):
        super().__init__()

        self.goB = QPushButton('Go')
        self.constructB = QPushButton('Construct game')
        self.stepOneB = QPushButton('Step 1')
        self.importMapB = QPushButton('Import Map')
        self.importRuleB = QPushButton('Import Rule')
        self.stepTenB = QPushButton('Step 10')
        self.pauseB = QPushButton('Pause')
        self.saveExportB = QPushButton('Save and export map')
        self.createRuleB = QPushButton('Create new Rule')

        #self.count = 7

        self.initLayout()

    def initLayout(self):

        self.simLayout = QGridLayout()

        self.simLayout.addWidget(self.goB,          *(0, 0))
        self.simLayout.addWidget(self.constructB,   *(1, 2))
        self.simLayout.addWidget(self.stepOneB,     *(0, 1))
        self.simLayout.addWidget(self.importMapB,   *(1, 0))
        self.simLayout.addWidget(self.importRuleB,  *(1, 1))
        self.simLayout.addWidget(self.stepTenB,     *(0, 2))
        self.simLayout.addWidget(self.pauseB,       *(2, 0))
        self.simLayout.addWidget(self.saveExportB,  *(2, 1))
        self.simLayout.addWidget(self.createRuleB,  *(2, 2))

        self.setLayout(self.simLayout)



class RuleUI(QWidget):
    def __init__(self):
        super().__init__()

        self.moorelian = True
        self.neighbourhoodSize = 3
        self.nStates = 2
        self.dimensions = 2
        self.centre = [1, 1]
        self.countCentre = False
        self.usePositionTree = False
        self.baseRule = 0

        self.rules = []

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        infoLayout = QVBoxLayout()
        valLayout = QVBoxLayout()
        widgLayout = QVBoxLayout()

        mooreBox = QComboBox()
        mooreBox.addItem("Moorelian")
        mooreBox.addItem("Von Neumann")
        mooreBox.activated[str].connect(self.setMoorelian)
        widgLayout.addWidget(mooreBox)
        mooreBoxInfo = QLabel("Moorelian neighbourhoods have diagonal cells as neighbours.\nVon Neumann neighbourhoods do not.")
        infoLayout.addWidget(mooreBoxInfo)
        self.mooreBoxVal = QLabel("Mode: Moorelian")
        valLayout.addWidget(self.mooreBoxVal)

        NHSize = QPushButton("Choose neighbourhood size")
        NHSize.clicked.connect(self.setNeighbourhoodSize)
        widgLayout.addWidget(NHSize)
        NHSizeInfo = QLabel("A neighbourhood size is the size of the grid.")
        infoLayout.addWidget(NHSizeInfo)
        self.NHSizeVal = QLabel("Size: 3")
        valLayout.addWidget(self.NHSizeVal)

        nStates = QPushButton("Choose number of cell states")
        nStates.clicked.connect(self.setnStates)
        widgLayout.addWidget(nStates)
        nStateInfo = QLabel("The number of cell states. For instance, binary has 2 states.")
        infoLayout.addWidget(nStateInfo)
        self.nStateVal = QLabel("States: 2")
        valLayout.addWidget(self.nStateVal)

        dimensions = QPushButton("Choose number of dimensions")
        dimensions.clicked.connect(self.setDimensions)
        widgLayout.addWidget(dimensions)
        dimensionsInfo = QLabel("The number of dimensions the rule can be used for.")
        infoLayout.addWidget(dimensionsInfo)
        self.dimensionsVal = QLabel("Dimensions: 2")
        valLayout.addWidget(self.dimensionsVal)

        centre = QPushButton("Choose centre location")
        centre.clicked.connect(self.setCentre)
        widgLayout.addWidget(centre)
        centreInfo = QLabel("I still don't know what centre is.")
        infoLayout.addWidget(centreInfo)
        self.centreVal = QLabel("Centre: [1, 1]")
        valLayout.addWidget(self.centreVal)

        countCentre = QComboBox()
        countCentre.addItem("No")
        countCentre.addItem("Yes")
        countCentre.activated[str].connect(self.setCountCentre)
        widgLayout.addWidget(countCentre)
        countCentreInfo = QLabel("A cell will include itself when counting adjacent cells to\ndetermine its life or death.")
        infoLayout.addWidget(countCentreInfo)
        self.countCentreVal = QLabel("Count Centre: False")
        valLayout.addWidget(self.countCentreVal)

        #Use position Tree

        baseRule = QComboBox()
        baseRule.addItem("Death")
        baseRule.addItem("Life")
        baseRule.activated[str].connect(self.setBaseRule)
        widgLayout.addWidget(baseRule)
        baseRuleInfo = QLabel("The default rule applied to a cell if no other rules apply.")
        infoLayout.addWidget(baseRuleInfo)
        self.baseRuleVal = QLabel("Base Rule: Death")
        valLayout.addWidget(self.baseRuleVal)

        layout.addLayout(infoLayout)
        layout.addLayout(valLayout)
        layout.addLayout(widgLayout)
        self.setLayout(layout)

    def setMoorelian(self, text):
        if text == "Moorelian":
            self.moorelian = True
            self.mooreBoxVal.setText("Mode: Moorelian")
        elif text == "Von Neumann":
            self.moorelian = False
            self.mooreBoxVal.setText("Mode: Von Neumann")

    def setNeighbourhoodSize(self):
        n, okPressed = QInputDialog.getInt(self, "Choose Neighbourhood Size", "Size:", self.neighbourhoodSize, 2, 999999, 1)
        if okPressed:
            self.neighbourhoodSize = n
            self.NHSizeVal.setText("Size: " + str(n))

    def setnStates(self):
        n, okPressed = QInputDialog.getInt(self, "Choose number of cell states", "Number:", self.nStates, 2, 999999, 1)
        if okPressed:
            self.nStates = n
            self.nStateVal.setText("States: " + str(n))

    def setDimensions(self):
        n, okPressed = QInputDialog.getInt(self, "Choose number of dimensions", "Number:", self.dimensions, 1, 999999, 1)
        if okPressed:
            self.dimensions = n
            self.dimensionsVal.setText("Dimensions: " + str(n))

    def setCentre(self):
        centre = []
        for i in range(self.dimensions):
            n, okPressed = self._setCentreIndex(i)
            if okPressed:
                centre.append(n)
            else:
                return
        self.centre = centre
        self.centreVal.setText("Centre: " + str(centre))

    def _setCentreIndex(self, i):
        return QInputDialog.getInt(self, "Choose center indices", "Index " + str(i) + "i", 1, 1, 999999, 1)


    def setCountCentre(self, text):
        if text == "No":
            self.countCentre = False
            self.countCentreVal.setText("Count Centre: False")
        elif text == "Yes":
            self.countCentre = True
            self.countCentreVal.setText("Count Centre: True")

    def setBaseRule(self, text):
        if text == "Death":
            self.baseRule = 0
            self.baseRuleVal.setText("Base Rule: Death")
        elif text == "Life":
            self.baseRule = 1
            self.baseRuleVal.setText("Base Rule: Life")

    # def addRule(self):
    #     state =

if __name__ == "__main__":
    pass