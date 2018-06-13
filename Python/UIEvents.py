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
        self.thread.goSignal.connect(self.stepForward)

    def pause(self):
        self.thread.terminate()
        self.statusBar().showMessage("Paused")

    def go(self):
        if self.time is not None:
            self.thread.start()
            self.statusBar().showMessage("Game running")

        else:
            self.statusBar().showMessage("Can't go")

    def exportMap(self):
        pass


    def createMap(self):
        moore, okPressed = QInputDialog.getItem(self, "Is the rule Moorelian?",
                                                "Moore neighboorhood: corners of cells count as adjacent",
                                                ('True', 'False'), 0, False)
        if okPressed:
            NHSize, okPressed = QInputDialog.getItem(self, "Set neighbourhood size",
                                                "Neighboorhood size: ?????????",
                                                ('hello', 'there'), 0, False)
            if okPressed:
                fname = QFileDialog.getSaveFileName(self, 'Save Rule', fileSystem.getProjectRoot(), "Rule files (*.rule)")
                print(fname)
                if fname[0]:
                    f = open(fname[0], 'w+')
                    f.write('moorelian:' + moore + '\n')
                    f.write('neighbourhoodSize:' + NHSize)

                    #load map
                    # self.map = fileSystem.loadMap(fname[0])
                    self.mapName.setText("Map: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])])
                    self.statusBar().showMessage("Rule creation successful")


    #Construct Game
    def constructGame(self):
        if self.map is not None and self.rule is not None:
            self.time = tempus.Time(self.map, self.rule)
            self.statusBar().showMessage("Constructed Game")


    #Import Rule
    def importRule(self):
        fname = QFileDialog.getOpenFileName(self, 'Import Rule', fileSystem.getProjectRoot(), "Rule files (*.rule)")
        if fname[0]:
            self.rule = fileSystem.loadRule(fname[0])
            self.ruleName.setText("Rule: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])])
            self.statusBar().showMessage("Rule: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])])

    #Import Map
    def importMap(self):
        fname = QFileDialog.getOpenFileName(self, 'Import Map', fileSystem.getProjectRoot(), "Map files (*.map)")
        if fname[0]:
            self.map = fileSystem.loadMap(fname[0])
            self.mapName.setText("Map: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])])
            self.statusBar().showMessage("Map: " + fname[0][fname[0].rfind('/') + 1:len(fname[0])])

    #Step Foward event
    def stepForward(self):
        if self.time is not None:
            self.time.step({'draw2D': True})


    def stepForwardTen(self):
        if self.time is not None:
            for _ in range(10):
                self.stepForward()
                time.sleep(0.01)




if __name__ == "__main__":
    pass