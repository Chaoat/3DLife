import sys
import time


from BorderLayout import BorderLayout as Bl
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QFileDialog,QLabel,
                             QMainWindow, QAction, qApp, QHBoxLayout, QGridLayout, QInputDialog, QComboBox)

import map, rule, fileSystem, tempus


class Threader(QThread):

    goSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            self.goSignal.emit()
            time.sleep(1)


class EventHandler:

    def __init__(self):
        self.thread = Threader()
        self.thread.goSignal.connect(self.step)

    def go(self):
        if self.time is not None:
            self.thread.start()
            self.statusBar().showMessage("Simulation running")

        else:
            self.statusBar().showMessage("Please generate a simulation")

    def pause(self):
        self.thread.terminate()
        self.statusBar().showMessage("Simulation paused")

    def step(self):
        if self.time is not None:
            self.time.step({'draw': True})

    def toggleDrawMode(self, pressed):
        self.pause()
        if pressed:
            self.time.setDrawMode(True)
            self.statusBar().showMessage('Draw mode: ON')
        else:
            self.time.setDrawMode(False)
            self.statusBar().showMessage('Draw mode: OFF')


    def exportMap(self):
        return
        self.pause()
        if self.time is not None:
            fname = QFileDialog.getSaveFileName(self, 'Export Map', fileSystem.getProjectRoot(), "Map files (*.map)")
            if fname[0]:
                f = open(fname[0], 'w+')
                mapArray = self.time.exportInfo()

                ##WRITE TO FILE##

                f.close()

    def createRule(self):
        self.ruleUI.show()


    def generateSimulation(self):
        if self.map is not None and self.rule is not None:
            try:
                self.time = tempus.Time(self.map, self.rule, self.speed, self.timeStates)
                self.currentSimL.setText("Current Simulation:\n\t" + self.mapNameL.text() + '\n\t' + self.ruleNameL.text()
                                         + '\n\t' + self.simSpeedL.text() + '\n\t' + self.pastStatesL.text())

                self.statusBar().showMessage("Simulation Generated")
            except:
                self.statusBar().showMessage("Simulation not valid. Please generate a valid simulation.")


    def importRule(self):
        fname = QFileDialog.getOpenFileName(self, 'Import Rule', fileSystem.getProjectRoot(), "Rule files (*.rule)")
        if fname[0]:
            self.rule = fileSystem.loadRule(fname[0])
            self.ruleNameL.setText("Rule: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])])
            self.statusBar().showMessage("Rule: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])] + " has been imported")

    def importMap(self):
        fname = QFileDialog.getOpenFileName(self, 'Import Map', fileSystem.getProjectRoot(), "Map files (*.map)")
        if fname[0]:
            self.map = fileSystem.loadMap(fname[0])
            self.mapNameL.setText("Map: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])])
            self.statusBar().showMessage("Map: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])] + " has been imported")

    def setSpeed(self):
        n, okPressed = QInputDialog.getInt(self, "Choose simulation speed", "Speed:", 10, 0, 999999, 1)
        if okPressed:
            self.speed = n
            self.simSpeedL.setText("Speed: "+ str(n) + " frame/sec")

    def setTimeStates(self):
        n, okPressed = QInputDialog.getInt(self, "Choose number of past states", "States:", 1, 1, 999999, 1)
        if okPressed:
            self.timeStates = n
            self.pastStatesL.setText("Past States"+ str(n))












if __name__ == "__main__":
    pass