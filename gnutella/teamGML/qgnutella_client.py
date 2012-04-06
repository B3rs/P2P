import sys
from PyQt4.QtGui import QApplication, QMainWindow
from ui.qgnutella_window import QGnutellaWindow

app = QApplication(sys.argv)
window = QGnutellaWindow()

window.show()

sys.exit(app.exec_())