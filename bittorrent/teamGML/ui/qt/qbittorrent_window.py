from PyQt4.QtGui import QMainWindow, QListWidgetItem, QTreeWidgetItem, QProgressBar, QMessageBox
from PyQt4.QtCore import QStringList, SIGNAL, Qt
from uimainwindow import Ui_MainWindow
from managers.filesmanager import FilesManager
import threading
from custom_utils.logging import klog

class QBittorrentWindow(QMainWindow):
    def __init__(self, request_emitter):

        self.request_emitter = request_emitter
        self.request_emitter.ui_handler = self

        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Show the shared files into the shared folder
        self._redraw_shared_files()

        self.ui.logoutGroupBox.setVisible(False)

        #Connect the signals to events
        self.ui.searchBtn.clicked.connect(self._searchBtnClicked)
        self.ui.resultsTreeWidget.itemDoubleClicked.connect(self._resultsTreeClicked)
        self.ui.reloadSharedFilesBtn.clicked.connect(self._reloadSharedFiles)
        self.ui.loginBtn.clicked.connect(self._login)
        self.ui.logoutBtn.clicked.connect(self._logout)

        self.connect(self, SIGNAL("shared_files_changed"), self._redraw_shared_files)
        self.connect(self, SIGNAL("new_result_file"), self._draw_new_result_file)

        self.connect(self, SIGNAL("download_file_changed"), self._draw_download_item)
        self.connect(self, SIGNAL("upload_file_changed"), self._draw_upload_item)

        self.connect(self, SIGNAL("log_message_ready"), self._show_log_message)

        self.connect(self, SIGNAL("login_done"), self._login_done)


    #EVENTS
    def _login(self):
        tracker_ip = self.ui.trackerIpLineEdit.text()
        tracker_port = self.ui.trackerPortLineEdit.text()

        if len(tracker_ip)>0 and len(tracker_port) > 0:
            self.ui.trackerStatusLabel.setText("Sto connettendo...")
            self.request_emitter.login(tracker_ip, tracker_port)


    def _logout(self):
        if self.request_emitter.logout() != -1:
            self.ui.trackerStatusLabel.setText("Disconnesso...")
            self.ui.logoutGroupBox.setVisible(False)
            self.ui.loginGroupBox.setVisible(True)
            self.ui.sessionIdLabel.setText("")
        else:
            self.ui.trackerStatusLabel.setText("Non puoi disconnetterti!")
            #After some seconds redraw "Connesso"
            threading.timer(3, self.ui.trackerStatusLabel.setText("Connesso")).start()

    def _login_done(self, session_id):
        try:
            if not session_id:
                self.ui.trackerStatusLabel.setText("Login non riuscito, forse il tracker non esiste.")
                return

            elif int(session_id) == 0:
                self.ui.trackerStatusLabel.setText("Il tracker non vuole farti loggare.")
                return

        except Exception:
            pass

        self.ui.sessionIdLabel.setText(session_id)
        self.ui.loginGroupBox.setVisible(False)
        self.ui.logoutGroupBox.setVisible(True)
        self.request_emitter.add_all_files_to_tracker()

    def _reloadSharedFiles(self):
        FilesManager.load_my_files()
        self._redraw_shared_files()
        self.request_emitter.add_all_files_to_tracker()

    def _show_log_message(self, message):
        self.ui.loggingTextBrowser.append(message)

    def _searchBtnClicked(self):
        self.ui.resultsTreeWidget.clear()
        query = self.ui.searchLineEdit.text()
        self.request_emitter.search_for_files(query)

    def _resultsTreeClicked(self, item, index):
        file_id = item.text(1)
        self.request_emitter.download_file(file_id)
        self.ui.tabsWidget.setCurrentIndex(4) #go to the transfer page


    def _redraw_shared_files(self):
        self.ui.sharedFilesListWidget.clear()
        for file in FilesManager.shared_files():
            file_item = QListWidgetItem(file.filename, self.ui.sharedFilesListWidget)

    def _draw_new_result_file(self, filename, file_id, file_size, part_size):
        item = QTreeWidgetItem(self.ui.resultsTreeWidget, QStringList([str(filename), str(file_id), str(file_size), str(part_size)]))

    def _draw_download_item(self, filename, id, part_number, peer_ip, percent):
        self._draw_transfer_item(self.ui.downloadsTreeWidget, filename, id, part_number, peer_ip, percent)

    def _draw_upload_item(self, filename, md5, peer_ip, percent):
        self._draw_transfer_item(self.ui.uploadsTreeWidget, filename, id, part_number, peer_ip, percent)

    def _draw_transfer_item(self, container, filename, id, part_number, peer_ip, percent):
        items_found = container.findItems(id, Qt.MatchExactly, 3)
        item = None
        if len(items_found) > 0:

            for i in items_found:
                if i.text(4) == peer_ip and i.text(1) == str(part_number):
                    item = i
                    break

        if item:
            container.itemWidget(item, 1).setValue(percent)
        else:
            item = QTreeWidgetItem(container, QStringList([str(filename), str(part_number), "0", str(id), str(peer_ip)]))
            progress_bar = QProgressBar()
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(100)
            progress_bar.setValue(percent)
            container.setItemWidget(item, 1, progress_bar)


    #PUBLIC Methods (ovverides from AbstractUI in the future)

    def add_new_result_file(self, filename, file_id, file_size, part_size):
        self.emit(SIGNAL("new_result_file"), filename, file_id, file_size, part_size)

    def shared_files_changed(self):
        self.emit(SIGNAL("shared_files_changed"))

    def download_file_changed(self, filename, file_id, part_number, peer_ip, percent):
        self.emit(SIGNAL("download_file_changed"), filename, file_id, part_number, peer_ip, percent)

    def upload_file_changed(self, filename, file_id, peer_ip, percent):
        self.emit(SIGNAL("upload_file_changed"), filename, file_id, peer_ip, percent)

    def show_log_message(self, message):
        self.emit(SIGNAL("log_message_ready"), message)

    def login_done(self, session_id):
        self.emit(SIGNAL("login_done"), session_id)
