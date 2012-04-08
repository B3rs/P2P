import sys
from PyQt4.QtGui import QApplication, QMainWindow
from ui.qt.qgnutella_window import QGnutellaWindow
from threads.response_handler_thread import ResponseHandlerThread
from threads.request_emitter_thread import RequestEmitterThread

PORT = 9999

if __name__ == "__main__":

    #Setup the emitter thread
    request_emitter = RequestEmitterThread(PORT)
    #TODO: RequestEmitterThread doesn't have a run method! WTF?!

    #Setup the UI
    app = QApplication(sys.argv)
    ui = QGnutellaWindow(request_emitter)

    # Launch background thread for network handling
    bg = ResponseHandlerThread(PORT, ui)
    bg.setDaemon(True)
    bg.start()

    ui.show()

    sys.exit(app.exec_())
