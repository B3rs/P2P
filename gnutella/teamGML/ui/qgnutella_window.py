from PyQt4.QtGui import QMainWindow, QListWidgetItem, QTreeWidgetItem
from PyQt4.QtCore import QStringList
from uimainwindow import Ui_MainWindow
from managers.filesmanager import FilesManager
from managers.peersmanager import PeersManager


class QGnutellaWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        #Show the shared files into the sharedfolder
        for file_name in FilesManager.shared_files():
            file_item = QListWidgetItem(file_name, self.ui.sharedFilesListWidget)

        #Show the known neighbours
        for peer in PeersManager.find_known_peers():
            item = QTreeWidgetItem(self.ui.peersTreeWidget, QStringList([str(peer.ip),str(peer.port)]))


        #Connect the signals to events
        self.ui.searchBtn.clicked.connect(self._searchBtnClicked)
        self.ui.resultsTreeWidget.itemDoubleClicked.connect(self._resultsTreeClicked)


    #EVENTS
    def _searchBtnClicked(self):
        query = self.ui.searchLineEdit.text()
        print query
        self.ui.resultsTreeWidget.clear()

    def _resultsTreeClicked(self, item, index):
        file_name = item.text(0)
        peer_ip = item.text(1)
        peer_port = item.text(2)
        print "Scarico: %s da %s:%s" % (file_name, peer_ip, peer_port)


    #PUBLIC Methods
    def add_new_result_file(self, filename, peer_ip, peer_port):
        item = QTreeWidgetItem(self.ui.resultsTreeWidget, QStringList([str(filename), str(peer_ip), str(peer_port)]))


