from PyQt4.QtGui import QMainWindow, QListWidgetItem, QTreeWidgetItem, QProgressBar, QMessageBox
from PyQt4.QtCore import QStringList, SIGNAL, Qt
from uimainwindow import Ui_MainWindow
from managers.filesmanager import FilesManager
from managers.peersmanager import PeersManager
from managers.usersmanager import UsersManager
from custom_utils.logging import klog
from models.peer import Peer

class QKazaaWindow(QMainWindow):
    def __init__(self, request_emitter, is_superpeer=False):

        self.request_emitter = request_emitter
        self.request_emitter.ui_handler = self

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Show the shared files into the shared folder
        self._redraw_shared_files()

        #Show the known neighbours
        self._redraw_neighbours_peers()

        #Change the UI based on is_superpeer
        if is_superpeer:
            self.ui.sessionGroupBox.setVisible(False)
            self.ui.youAreLabel.setText("superpeer")
        else:
            self.ui.youAreLabel.setText("peer")
            self.ui.tabsWidget.removeTab(2) #remove the "My peers" tab

        self.ui.logoutBtn.setVisible(False)

        #Connect the signals to events
        self.ui.searchBtn.clicked.connect(self._searchBtnClicked)
        self.ui.resultsTreeWidget.itemDoubleClicked.connect(self._resultsTreeClicked)
        self.ui.addNeighbourPeerBtn.clicked.connect(self._addNeighourPeerBtnClicked)
        self.ui.searchSuperPeerBtn.clicked.connect(self._searchSuperPeerBtnClicked)
        self.ui.clearNeighboursBtn.clicked.connect(self._clearAllNeighbours)
        self.ui.reloadSharedFilesBtn.clicked.connect(self._reloadSharedFiles)
        self.ui.logoutBtn.clicked.connect(self._logout)

        self.connect(self, SIGNAL("neighbours_peers_changed"), self._redraw_neighbours_peers)
        self.connect(self, SIGNAL("shared_files_changed"), self._redraw_shared_files)
        self.connect(self, SIGNAL("new_result_file"), self._draw_new_result_file)

        self.connect(self, SIGNAL("download_file_changed"), self._draw_download_item)
        self.connect(self, SIGNAL("upload_file_changed"), self._draw_upload_item)

        self.connect(self, SIGNAL("log_message_ready"), self._show_log_message)

        self.connect(self, SIGNAL("superpeer_choosen"), self._show_choosen_superpeer)
        self.connect(self, SIGNAL("new_superpeer"), self._draw_new_superpeer)
        self.connect(self, SIGNAL("new_peer"), self._draw_new_peer)
        self.connect(self, SIGNAL("remove_peer"), self._remove_peer)

        self.connect(self, SIGNAL("login_done"), self._login_done)


    #EVENTS

    def _logout(self):
        if self.request_emitter.logout() != -1:
            self.ui.logoutBtn.setVisible(False)
            self.ui.searchSuperPeerBtn.setVisible(True)
            self.ui.sessionIdLabel.setText("")
            self.ui.superPeerLabel.setText("")

    def _login_done(self, session_id):
        try:
            if int(session_id) == 0:
                self.ui.sessionIdLabel.setText("Errore, esisti gia nel supernodo.")
                return
        except Exception:
            pass

        self.ui.sessionIdLabel.setText(session_id)
        self.request_emitter.register_all_files_to_supernode()

    def _clearAllNeighbours(self):
        PeersManager.remove_all_peers()
        self.ui.neighboursPeersTreeWidget.clear()

    def _reloadSharedFiles(self):
        self.request_emitter.unregister_all_files_to_supernode()
        FilesManager.load_my_files()
        self._redraw_shared_files()
        self.request_emitter.register_all_files_to_supernode()


    def _draw_new_superpeer(self, superpeer_ip, superpeer_port):
        item = QTreeWidgetItem(self.ui.superpeersTreeWidget, QStringList([str(superpeer_ip), str(superpeer_port)]))

    def _remove_peer(self, peer_ip, peer_port):
        items_found = self.ui.mypeersTreeWidget.findItems(peer_ip, Qt.MatchExactly, 0)

        if len(items_found) > 0:

            #search the port
            for i in items_found:
                if i.text(1) == peer_port:
                    self.ui.mypeersTreeWidget.removeItemWidget(i, 0)
                    self.ui.mypeersTreeWidget.removeItemWidget(i, 1)


    def _draw_new_peer(self, peer_ip, peer_port):
        item = QTreeWidgetItem(self.ui.mypeersTreeWidget, QStringList([str(peer_ip), str(peer_port)]))

    def _show_choosen_superpeer(self, ip, port):
        self.ui.superPeerLabel.setText("%s:%d" %(ip, int(port)))
        self.ui.logoutBtn.setVisible(True)
        self.ui.searchSuperPeerBtn.setVisible(False)

    def _show_log_message(self, message):
        self.ui.loggingTextBrowser.append(message)

    def _searchSuperPeerBtnClicked(self):
        self.ui.superpeersTreeWidget.clear()
        self.request_emitter.search_for_superpeers()

    def _addNeighourPeerBtnClicked(self):
        ip = self.ui.peerIP.text()
        port = self.ui.peerPort.text()

        if len(port) > 1 and len(ip.split(".")) == 4:
            # Add peer to PeerManager and to list
            PeersManager.add_new_peer(Peer(ip, port))
            self.neighbours_peers_changed()

    def _searchBtnClicked(self):
        self.ui.resultsTreeWidget.clear()
        query = self.ui.searchLineEdit.text()
        ttl = int(self.ui.ttlFilesSearchSpinBox.value())
        self.request_emitter.search_for_files(query, ttl)

    def _resultsTreeClicked(self, item, index):
        file_name = item.text(0)
        peer_ip = item.text(1)
        peer_port = item.text(2)
        file_md5 = item.text(3)
        klog("Scarico: %s da %s:%s" % (file_name, peer_ip, peer_port))
        self.request_emitter.download_file(peer_ip, peer_port, file_md5, file_name)
        self.ui.tabsWidget.setCurrentIndex(3) #go to the transfer page


    def _redraw_neighbours_peers(self):
        self.ui.neighboursPeersTreeWidget.clear()
        for peer in PeersManager.find_known_peers():
            item = QTreeWidgetItem(self.ui.neighboursPeersTreeWidget, QStringList([str(peer.ip),str(peer.port)]))

    def _redraw_shared_files(self):
        self.ui.sharedFilesListWidget.clear()
        for file in FilesManager.shared_files():
            file_item = QListWidgetItem(file.filename, self.ui.sharedFilesListWidget)

    def _draw_new_result_file(self, filename, peer_ip, peer_port, file_md5):
        item = QTreeWidgetItem(self.ui.resultsTreeWidget, QStringList([str(filename), str(peer_ip), str(peer_port), str(file_md5)]))

    def _draw_download_item(self, filename, md5, peer_ip, percent):
        self._draw_transfer_item(self.ui.downloadsTreeWidget, filename, md5, peer_ip, percent)

    def _draw_upload_item(self, filename, md5, peer_ip, percent):
        self._draw_transfer_item(self.ui.uploadsTreeWidget, filename, md5, peer_ip, percent)

    def _draw_transfer_item(self, container, filename, md5, peer_ip, percent):
        items_found = container.findItems(md5, Qt.MatchExactly, 3)
        item = None
        if len(items_found) > 0:

            for i in items_found:
                if i.text(2) == peer_ip:
                    item = i
                    break

        if item:
            container.itemWidget(item, 1).setValue(percent)
        else:
            item = QTreeWidgetItem(container, QStringList([str(filename), "0", str(peer_ip), str(md5)]))
            progress_bar = QProgressBar()
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(100)
            progress_bar.setValue(percent)
            container.setItemWidget(item, 1, progress_bar)


    #PUBLIC Methods (ovverides from AbstractUI in the future)

    def add_new_result_file(self, filename, peer_ip, peer_port, file_md5):
        self.emit(SIGNAL("new_result_file"), filename, peer_ip, peer_port, file_md5)

    def neighbours_peers_changed(self):
        self.emit(SIGNAL("neighbours_peers_changed"))

    def shared_files_changed(self):
        self.emit(SIGNAL("shared_files_changed"))

    def download_file_changed(self, filename, file_md5, peer_ip, percent):
        self.emit(SIGNAL("download_file_changed"), filename, file_md5, peer_ip, percent)

    def upload_file_changed(self, filename, file_md5, peer_ip, percent):
        self.emit(SIGNAL("upload_file_changed"), filename, file_md5, peer_ip, percent)

    def show_log_message(self, message):
        self.emit(SIGNAL("log_message_ready"), message)

    def superpeer_choosen(self, ip, port):
        self.emit(SIGNAL("superpeer_choosen"), ip, port)

    def add_new_superpeer(self, ip, port):
        self.emit(SIGNAL("new_superpeer"), ip, port)

    def add_new_peer(self, ip, port):
        self.emit(SIGNAL("new_peer"), ip, port)

    def remove_peer(self, ip, port):
        self.emit(SIGNAL("remove_peer"), ip, port)

    def login_done(self, session_id):
        self.emit(SIGNAL("login_done"), session_id)



