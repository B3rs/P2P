from PyQt4.QtGui import QMainWindow, QListWidgetItem, QTreeWidgetItem
from PyQt4.QtCore import QStringList
from uimainwindow import Ui_MainWindow
from managers.filesmanager import FilesManager
from managers.peersmanager import PeersManager
from ui.abstract_ui import AbstractGnutellaUI


class QGnutellaWindow(QMainWindow):
    def __init__(self, request_emitter):

        self.request_emitter = request_emitter

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Show the shared files into the sharedfolder
        for file_name in FilesManager.shared_files():
            file_item = QListWidgetItem(file_name, self.ui.sharedFilesListWidget)

        #Show the known neighbours
        self.peers_changed()

        #Connect the signals to events
        self.ui.searchBtn.clicked.connect(self._searchBtnClicked)
        self.ui.resultsTreeWidget.itemDoubleClicked.connect(self._resultsTreeClicked)
        self.ui.searchNeighboursBtn.clicked.connect(self._searchNeighboursBtnClicked)

    #EVENTS
    def _searchBtnClicked(self):
        self.ui.resultsTreeWidget.clear()
        query = self.ui.searchLineEdit.text()
        self.request_emitter.search_for_files(query)

    def _resultsTreeClicked(self, item, index):
        file_name = item.text(0)
        peer_ip = item.text(1)
        peer_port = item.text(2)
        file_md5 = item.text(3)
        print "Scarico: %s da %s:%s" % (file_name, peer_ip, peer_port)
        self.request_emitter.download_file(peer_ip, peer_port, file_md5)

    def _searchNeighboursBtnClicked(self):
        self.request_emitter.search_for_peers()


    #PUBLIC Methods (ovverides from AbstractUI in the future)
    def add_new_result_file(self, filename, peer_ip, peer_port, file_md5):
        item = QTreeWidgetItem(self.ui.resultsTreeWidget, QStringList([str(filename), str(peer_ip), str(peer_port), str(file_md5)]))

    def peers_changed(self):
        for peer in PeersManager.find_known_peers():
            item = QTreeWidgetItem(self.ui.peersTreeWidget, QStringList([str(peer.ip),str(peer.port)]))

