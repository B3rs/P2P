__author__ = 'maurizio'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from bittorrent.teamFGM.GUIka.Splash_GUIka import Ui_MainWindow
import sys

class SplashGUIkaUse(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.splashUi = Ui_MainWindow()
        self.splashUi.setupUi(self)

        self.startNode = False
        self.startSupernode = False

        #Connect the signals to events
        self.splashUi.Splash_nodeBtn.clicked.connect(self._NodeBtnClicked)
        self.splashUi.Splash_SUPERnodeBtn.clicked.connect(self._SuperNodeBtnClicked)
        self.splashUi.Splash_NothingBtn.clicked.connect(self._NothingBtnClicked)

    #Events definition
    def _NodeBtnClicked(self):
        self.startNode = True

    def _SuperNodeBtnClicked(self):
        self.startSupernode = True

    def _NothingBtnClicked(self):
        sys.exit(app.exec_())

