import sys
from PyQt4.QtGui import QApplication, QMainWindow
from ui.qt.qgnutella_window import QGnutellaWindow
from threads.response_handler_thread import ResponseHandlerThread
from threads.request_emitter import RequestEmitter
from managers.filesmanager import FilesManager
from custom_utils import logging

PORT = 8000

if __name__ == "__main__":

    FilesManager.load_files()
    #Setup the emitter thread
    request_emitter = RequestEmitter(PORT)
    #TODO: RequestEmitterThread doesn't have a run method! WTF?!

    #Setup the UI
    app = QApplication(sys.argv)
    ui = QGnutellaWindow(request_emitter)

    #Set the UI to the logger function to show the log messages also in the UI
    logging.UI_LOGGER = ui

    # Launch background thread for network handling
    bg = ResponseHandlerThread(PORT, ui)
    bg.daemon = True
    bg.start()

    ui.show()

    sys.exit(app.exec_())
