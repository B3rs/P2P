from PyQt4.QtGui import QMainWindow, QListWidgetItem, QTreeWidgetItem, QProgressBar
from PyQt4.QtCore import QStringList, SIGNAL, Qt
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

        #Show the shared files into the shared folder
        self._redraw_shared_files()

        #Show the known neighbours
        self._redraw_peers()

        #Connect the signals to events
        self.ui.searchBtn.clicked.connect(self._searchBtnClicked)
        self.ui.resultsTreeWidget.itemDoubleClicked.connect(self._resultsTreeClicked)
        self.ui.searchNeighboursBtn.clicked.connect(self._searchNeighboursBtnClicked)
        self.ui.addPeerBtn.clicked.connect(self._addPeerBtnClicked)
        self.connect(self, SIGNAL("peers_changed"), self._redraw_peers)
        self.connect(self, SIGNAL("shared_files_changed"), self._redraw_shared_files)
        self.connect(self, SIGNAL("new_result_file"), self._draw_new_result_file)

        self.connect(self, SIGNAL("download_file_changed"), self._draw_download_item)
        self.connect(self, SIGNAL("upload_file_changed"), self._draw_upload_item)

        self._draw_download_item("cane", "1212", "10.0.0.1", 0)
        self._draw_download_item("cane", "1212", "10.0.0.1", 50)
        self._draw_upload_item("pene", "2", "22.0.0.1", 0)
        self._draw_upload_item("pene", "2", "22.0.0.1", 60)

    #EVENTS
    def _addPeerBtnClicked(self):
        ip = self.ui.peerIP.text()
        port = self.ui.peerPort.text()

        if len(port) > 1 and len(ip.split(".")) == 4:
            # Add peer to PeerManager and to list
            PeersManager.add_new_peer(ip, port)
            self.peers_changed()

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

    #EVENTS HANDLING
    def _searchNeighboursBtnClicked(self):
        self.request_emitter.search_for_peers()

    def _redraw_peers(self):
        self.ui.peersTreeWidget.clear()
        for peer in PeersManager.find_known_peers():
            item = QTreeWidgetItem(self.ui.peersTreeWidget, QStringList([str(peer.ip),str(peer.port)]))

    def _redraw_shared_files(self):
        self.ui.sharedFilesListWidget.clear()
        for file_name in FilesManager.shared_files():
            file_item = QListWidgetItem(file_name, self.ui.sharedFilesListWidget)

    def _draw_new_result_file(self, filename, peer_ip, peer_port, file_md5):
        item = QTreeWidgetItem(self.ui.resultsTreeWidget, QStringList([str(filename), str(peer_ip), str(peer_port), str(file_md5)]))

    def _draw_download_item(self, filename, md5, peer_ip, percent):
        self._draw_transfer_item(self.ui.downloadsTreeWidget, filename, md5, peer_ip, percent)

    def _draw_upload_item(self, filename, md5, peer_ip, percent):
        self._draw_transfer_item(self.ui.uploadsTreeWidget, filename, md5, peer_ip, percent)

    def _draw_transfer_item(self, container, filename, md5, peer_ip, percent):
        #QTreeWidget::setItemWidget ( QTreeWidgetItem * item, int column, QWidget * widget )
        items_found = container.findItems(md5, Qt.MatchExactly, 3)
        if len(items_found) > 0:
            item = items_found[0]
            container.itemWidget(item, 1).setValue(percent)
        else:
            item = QTreeWidgetItem(container, QStringList([str(filename), "0%", str(peer_ip), str(md5)]))
            progress_bar = QProgressBar()
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(100)
            progress_bar.setValue(percent)
            container.setItemWidget(item, 1, progress_bar)


    #PUBLIC Methods (ovverides from AbstractUI in the future)

    def add_new_result_file(self, filename, peer_ip, peer_port, file_md5):
        self.emit(SIGNAL("new_result_file"), filename, peer_ip, peer_port, file_md5)

    def peers_changed(self):
        self.emit(SIGNAL("peers_changed"))

    def shared_files_changed(self):
        self.emit(SIGNAL("shared_files_changed"))

    def download_file_changed(self, filename, peer_ip, peer_port, file_md5):
        self.emit(SIGNAL("download_file_changed"), filename, peer_ip, peer_port, file_md5)

    def upload_file_changed(self, filename, peer_ip, peer_port, file_md5):
        self.emit(SIGNAL("upload_file_changed"), filename, peer_ip, peer_port, file_md5)




