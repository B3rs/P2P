__author__ = 'maurizio'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Splash_GUIka import Ui_MainWindow
from Node_GUIka import Ui_NodeWindow
from SuperNode_GUIka import Ui_SuperNode

class GUIkaUse(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.splashUi = Ui_MainWindow()
        self.splashUi.setupUi(self)

        self.superNodeUi = Ui_SuperNode()
        self.superNodeUi.setupUi(self)

        #Connect the signals to events
        self.splashUi.Splash_nodeBtn.clicked.connect(self._NodeBtnClicked)
        self.splashUi.Splash_SUPERnodeBtn.clicked.connect(self._SuperNodeBtnClicked)
        self.splashUi.Splash_NothingBtn.clicked.connect(self._NothingBtnClicked)

    #Events definition
    def _NodeBtnClicked(self,message):
        self.splashUi.Splash_statusbar.


        self.splashUi.Splash_nodeBtn
        self.superNodeUi.ChangeSuperNode_Btn.

