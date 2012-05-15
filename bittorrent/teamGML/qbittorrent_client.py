import sys
from PyQt4.QtGui import QApplication, QMainWindow, QMessageBox
from ui.qt.bittorrent_window import QBittorrentWindow
from threads.response_handler_thread import ResponseHandlerThread
from threads.request_emitter import RequestEmitter
from managers.filesmanager import FilesManager
from managers.usersmanager import UsersManager
from custom_utils import logging

PORT = 8000


def _ask_for_peer_role():
    msg_box = QMessageBox()
    msg_box.setText("Are you a super peer?")
    msg_box.addButton(QMessageBox.Yes)
    msg_box.addButton(QMessageBox.No)

    msg_box.show()
    msg_box.raise_()

    selection = msg_box.exec_()

    is_superpeer = (selection == QMessageBox.Yes)
    UsersManager.set_is_super_node(is_superpeer)

    return is_superpeer

if __name__ == "__main__":

    FilesManager.load_my_files()


    #Setup the UI
    app = QApplication(sys.argv)

    #Setup the emitter thread
    is_superpeer = _ask_for_peer_role()
    if is_superpeer:
        PORT = 80
    request_emitter = RequestEmitter(PORT)

    ui = QBittorrentWindow(request_emitter, is_superpeer)

    #Set the UI to the logger function to show the log messages also in the UI
    logging.UI_LOGGER = ui

    # Launch background thread for network handling
    bg = ResponseHandlerThread(PORT, ui)
    bg.daemon = True
    bg.start()

    ui.show()
    ui.raise_()

    sys.exit(app.exec_())
