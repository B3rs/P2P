__author__ = 'maurizio'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from bittorrent.teamFGM.GUIka.Node_GUIka import Ui_NodeWindow

class SplashGUIkaUse(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)

        self.startNode = False

        # Set up the user interface from Designer.
        self.nodeUi = Ui_NodeWindow
        self.nodeUi.setupUi(self)

        self.nodeUi.Node_ActualSuperNode_IP_text.setText("waiting")
        self.nodeUi.Node_ActualSuperNode_Port_text("...")

        #Connect the signals to events
        self.nodeUi.Node_START_Btn.clicked.connect(self._StartBtnClicked)
        self.nodeUi.Node_ChangeSuperNode_Btn.clicked.connect(self._ChangeSuperNodeBtnClicked)

    #Events definition
    def _StartBtnClicked(self):
        ip = self.nodeUi.Node_Root_IP.text()
        port = self.nodeUi.Node_Root_Port.text()

        if len(port) > 1 and len(ip.split(".")) == 4:
            # Add peer to PeerManager and to list
            self.ip = ip
            self.port = port
            self.startNode = True

    def __ChangeSuperNodeBtnClicked(self):
        ttl = self.nodeUi.Node_TTL_FindNeigh.text()
        if ttl > 0:
            self.searchSuperNode(ttl)




    #Public Methods

    def newSupernode(self,ip,port):
        self.nodeUi.Node_ActualSuperNode_IP_text.setText(ip)
        self.nodeUi.Node_ActualSuperNode_Port_text(port)

    def searchSuperNode(self,ttl):
        self.ttl = ttl

    def updateSuperList(self,QueryTable):
        self.nodeUi.Node_Neigh_tree. #TODO: inserire il risultato della ricerca nella tabella


