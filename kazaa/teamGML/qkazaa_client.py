import sys
from PyQt4.QtGui import QApplication, QMainWindow
from ui.qt.qkazaa_window import QKazaaWindow
from threads.response_handler_thread import ResponseHandlerThread
from threads.request_emitter import RequestEmitter
from managers.filesmanager import FilesManager
from custom_utils import logging

PORT = 8000

if __name__ == "__main__":

    FilesManager.load_my_files()

    #Setup the emitter thread
    request_emitter = RequestEmitter(PORT)

    #Setup the UI
    app = QApplication(sys.argv)
    ui = QKazaaWindow(request_emitter)

    #Set the UI to the logger function to show the log messages also in the UI
    logging.UI_LOGGER = ui

    # Launch background thread for network handling
    bg = ResponseHandlerThread(False, PORT, ui)
    bg.daemon = True
    bg.start()

    ui.show()

    sys.exit(app.exec_())
