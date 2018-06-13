import sys
import time


from BorderLayout import BorderLayout as Bl
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QFileDialog,QLabel,
                             QMainWindow, QAction, qApp, QHBoxLayout, QGridLayout, QInputDialog, QComboBox)

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


if __name__ == "__main__":
    pass