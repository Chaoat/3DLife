import sys
import time


from BorderLayout import BorderLayout as Bl
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QFileDialog,QLabel,
                             QMainWindow, QAction, qApp, QHBoxLayout, QGridLayout, QInputDialog, QComboBox,
                             QVBoxLayout, QCheckBox, QLineEdit, QMessageBox)

import map, rule, fileSystem, tempus



class RuleUI(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.moorelian = True
        self.neighbourhoodSize = 3
        self.nStates = 2
        self.dimensions = 2
        self.centre = [1, 1]
        self.countCentre = False
        self.usePositionTree = False
        self.baseRule = 0

        self.conditionSet = []
        self.conditionLabels = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Create Rule")
        self.move(550,600)

        layout = QHBoxLayout()

        infoLayout = QVBoxLayout()
        valLayout = QVBoxLayout()
        widgLayout = QVBoxLayout()

        moore = QPushButton("Choose neighbourhood mode")
        moore.clicked.connect(self.setMoorelian)
        widgLayout.addWidget(moore)
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
        centreInfo = QLabel("The center cell is the cell that is updated in the neighbourhood.")
        infoLayout.addWidget(centreInfo)
        self.centreVal = QLabel("Centre: [1, 1]")
        valLayout.addWidget(self.centreVal)

        countCentre = QPushButton("Choose count centre")
        countCentre.clicked.connect(self.setCountCentre)
        widgLayout.addWidget(countCentre)
        countCentreInfo = QLabel("A cell will include itself when counting adjacent cells to\ndetermine its life or death.")
        infoLayout.addWidget(countCentreInfo)
        self.countCentreVal = QLabel("Count Centre: False")
        valLayout.addWidget(self.countCentreVal)

        #Use position Tree

        baseCondition = QPushButton("Choose base condition")
        baseCondition.clicked.connect(self.setBaseRule)
        widgLayout.addWidget(baseCondition)
        baseRuleInfo = QLabel("The default condition applied to a cell if no other rules apply.")
        infoLayout.addWidget(baseRuleInfo)
        self.baseRuleVal = QLabel("Base Condition: 0")
        valLayout.addWidget(self.baseRuleVal)

        ruleSet = QPushButton("Add a condition")
        ruleSet.clicked.connect(self.addCondition)
        widgLayout.addWidget(ruleSet)
        ruleSetInfo = QLabel("Apply a condition to a cell state to change to another cell state")
        infoLayout.addWidget(ruleSetInfo)
        self.conditionSetVal = QLabel("Number of conditions: 0")
        valLayout.addWidget(self.conditionSetVal)


        self.ruleLayout = QVBoxLayout()

        resetConditions = QPushButton("Remove all conditions")
        resetConditions.clicked.connect(self.resetConditions)
        self.ruleLayout.addWidget(resetConditions)
        self.ruleLayout.addStretch(1)
        self.ruleLayout.addWidget(QLabel("Created Conditions"))


        fileLayout = QVBoxLayout()

        fileLayout.addStretch(1)
        importRule = QPushButton("Import and edit Rule")
        importRule.clicked.connect(self.importRule)
        fileLayout.addWidget(importRule)
        exportRule = QPushButton("Construct and save Rule")
        exportRule.clicked.connect(self.exportRule)
        fileLayout.addWidget(exportRule)


        layout.addLayout(infoLayout)
        layout.addLayout(widgLayout)
        layout.addLayout(valLayout)
        layout.addLayout(self.ruleLayout)
        layout.addLayout(fileLayout)
        self.setLayout(layout)


    def setMoorelian(self):
        options = ("Moorelian", "Von Neumann")
        text, okPressed = QInputDialog.getItem(self, "Choose Mode", "Mode:", options, 0, False)
        if okPressed:
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
        return QInputDialog.getInt(self, "Choose center indices", "Index: " + str(i), 1, 1, 999999, 1)

    def setCountCentre(self):
        options = ("No", "Yes")
        text, okPressed = QInputDialog.getItem(self, "Count centre", "Count centre:", options, 0, False)
        if okPressed:
            if text == "No":
                self.countCentre = False
                self.countCentreVal.setText("Count Centre: False")
            elif text == "Yes":
                self.countCentre = True
                self.countCentreVal.setText("Count Centre: True")

    def setBaseRule(self, text):
        n, okPressed = QInputDialog.getInt(self, "Choose base condition", "Condition:", 0, 0, self.nStates, 1)
        if okPressed:
            self.baseRule = n
            self.baseRuleVal.setText("Base Condition: " + str(n))

    def addCondition(self):
        self.addConditionDialog = addConditionDialog(self, self.nStates)
        self.addConditionDialog.show()

    def importRule(self):
        fname = QFileDialog.getOpenFileName(self, 'Import Rule', fileSystem.getProjectRoot(), "Rule files (*.rule)")
        if fname[0]:
            f = open(fname[0], "r")

            moore = f.readline().split(':')[1]
            if moore.lower() == 'true':
                moore = True
            else:
                moore = False

            if moore:
                self.moorelian = True
                self.mooreBoxVal.setText("Mode: Moorelian")
            else:
                self.moorelian = False
                self.mooreBoxVal.setText("Mode: Von Neumann")

            nhsize = int(f.readline().split(':')[1])
            self.neighbourhoodSize = nhsize
            self.NHSizeVal.setText("Size: " + str(nhsize))

            nstates = int(f.readline().split(':')[1])
            self.nStates = nstates
            self.nStateVal.setText("States: " + str(nstates))

            centre = f.readline().split(':')[1].split(', ')
            for i in range(len(centre)):
                centre[i] = int(centre[i])
            self.centre = centre
            self.centreVal.setText("Centre: " + str(centre))
            self.dimensions = len(centre)
            self.dimensionsVal.setText("Dimensions: " + str(len(centre)))

            countcentre = f.readline().split(':')[1]
            if countcentre.lower() == 'true':
                countcentre = True
            else:
                countcentre = False

            if not countcentre:
                self.countCentre = False
                self.countCentreVal.setText("Count Centre: False")
            else:
                self.countCentre = True
                self.countCentreVal.setText("Count Centre: True")

            f.readline()
            f.readline()        #use position tree

            baserule = int(f.readline().split(':')[1])
            self.baseRule = baserule
            self.baseRuleVal.setText("Base Condition: " + str(baserule))

            while True:
                line = f.readline()
                if line == '\n':
                    break
                condition = line.strip('\n')
                self.conditionSet.append(condition)
                self.conditionSetVal.setText("Number of conditions: " + str(len(self.conditionSet)))
                label = QLabel(condition)
                self.ruleLayout.addWidget(label)
                self.conditionLabels.append(label)

    def exportRule(self):
        fname = QFileDialog.getSaveFileName(self, 'Save Rule', fileSystem.getProjectRoot(), "Rule files (*.rule)")
        if fname[0]:
            f = open(fname[0], 'w+')
            f.write('moorelian:' + str(self.moorelian).upper() + '\n')
            f.write('neighbourhoodSize:' + str(self.neighbourhoodSize) + '\n')
            f.write('nStates:' + str(self.nStates) + '\n')
            s = ''
            for i in self.centre:
                s += str(i) + ', '
            s = s[:-2]
            f.write('center:' + s + '\n')
            f.write('countCenter:' + str(self.countCentre).upper() + '\n')

            f.write('\n')

            f.write("usePositionTree:" + str(self.usePositionTree).upper() + '\n')
            f.write('baseRule:' + str(self.baseRule) + '\n')
            for s in self.conditionSet:
                f.write(s + '\n')

            f.write('\n')

            f.write("CenterStates(seperated by commas):NeighbourNumbers(seperated by commas):ResultingState ##Don't remove this line##")

            f.close()

            self.parent.rule = fileSystem.loadRule(fname[0])
            self.parent.ruleName.setText("Rule: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])])
            self.parent.statusBar().showMessage("Rule: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])])

            self.close()

    def resetConditions(self):
        if len(self.conditionSet) > 0:
            remove = QMessageBox.question(self, "Remove conditions", "Are you sure you want to remove conditions?", QMessageBox.Yes
                                          |QMessageBox.No, QMessageBox.No)
            if remove == QMessageBox.No:
                return
            else:
                self.conditionSet = []
                self.conditionSetVal.setText("Number of conditions: 0")

                for label in self.conditionLabels:
                    label.close()
                    self.ruleLayout.removeWidget(label)
                self.conditionLabels = []









class addConditionDialog(QWidget):
    def __init__(self, parent, nStates):
        super().__init__()
        self.parent = parent

        self.nStates = nStates

        self.startStates = [0]*nStates
        self.endState = 0

        self.minLineEdits = [None] * nStates
        self.maxLineEdits = [None] * nStates

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Create Condition")
        self.move(550, 600)

        SSLayout = QVBoxLayout()
        SSLabel = QLabel("Start States:")
        SSLayout.addWidget(SSLabel)
        for i in range(self.nStates):
            stateCheckBox = QCheckBox(str(i))
            stateCheckBox.stateChanged.connect(self.setStartStates)
            SSLayout.addWidget(stateCheckBox)
        SSLayout.addStretch(1)

        ESLayout = QVBoxLayout()
        ESLabel = QLabel("End State:")
        ESLayout.addWidget(ESLabel)
        ESComboBox = QComboBox()
        for i in range(self.nStates):
            ESComboBox.addItem(str(i))
        ESComboBox.activated[str].connect(self.setEndState)
        ESLayout.addWidget(ESComboBox)
        ESLayout.addStretch(1)

        stateLayout = QHBoxLayout()
        stateLayout.addLayout(SSLayout)
        stateLayout.addLayout(ESLayout)


        NLabel = QLabel("Neighbours of each state:")
        NDataLayout = QGridLayout()
        Min = QLabel('Min')
        Max = QLabel('Max')
        NDataLayout.addWidget(Min,  *(0, 1))
        NDataLayout.addWidget(Max,  *(0, 2))
        for i in range(1, self.nStates):
            iLabel = QLabel(str(i) + ':')
            NDataLayout.addWidget(iLabel,   *(i, 0))
            minLabel = QLineEdit()
            self.minLineEdits[i] = minLabel
            NDataLayout.addWidget(minLabel, *(i, 1))
            maxLabel = QLineEdit()
            self.maxLineEdits[i] = maxLabel
            NDataLayout.addWidget(maxLabel, *(i, 2))
        NLayout = QVBoxLayout()
        NLayout.addWidget(NLabel)
        NLayout.addLayout(NDataLayout)

        BLayout = QHBoxLayout()
        cancelB = QPushButton("Cancel")
        cancelB.clicked.connect(self.cancel)
        BLayout.addWidget(cancelB)
        applyB = QPushButton("Apply")
        applyB.clicked.connect(self.applyCondition)
        BLayout.addWidget(applyB)

        layout = QVBoxLayout()
        layout.addLayout(stateLayout)
        layout.addLayout(NLayout)
        layout.addStretch(1)
        layout.addLayout(BLayout)

        self.setLayout(layout)


    def setStartStates(self, checked):
        source = self.sender()
        text = int(source.text())

        if checked == Qt.Checked:
            self.startStates[text] = 1
        else:
            self.startStates[text] = 0


    def setEndState(self, endState):
        self.endState = int(endState)

    def applyCondition(self):
        condition = ''

        accept = False
        for i in range(len(self.startStates)):
            if self.startStates[i] == 1:
                accept = True
                condition += str(i)
                condition += ','
        if not accept:
            return
        condition = condition[:-1]
        condition += ':'

        for i in range(1, self.nStates):                #don't include neighbours of state type 0
            try:
                min = self.minLineEdits[i].text()         #AttributeError
                max = self.maxLineEdits[i].text()
                imin = int(min)                         #ValueError
                imax = int(max)
                assert (imax >= imin)                   #AssertionError
            except (ValueError, AssertionError, AttributeError):
                return
            if imin == imax:
                condition += min + ','
            else:
                condition += min + '-' + max + ','
        condition = condition[:-1]
        condition += ':'

        condition += str(self.endState)

        self.parent.conditionSet.append(condition)
        self.parent.conditionSetVal.setText("Number of conditions: " + str(len(self.parent.conditionSet)))
        label = QLabel(condition)
        self.parent.ruleLayout.addWidget(label)
        self.parent.conditionLabels.append(label)

        self.close()

    def cancel(self):
        self.close()

if __name__ == "__main__":
    pass