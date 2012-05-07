__author__ = 'maurizio'

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Splash_GUIka.ui'
#
# Created: Thu Apr 26 20:55:34 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(519, 294)
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "FGMteamCreation", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.TitleLabel = QtGui.QLabel(self.centralwidget)
        self.TitleLabel.setGeometry(QtCore.QRect(21, 7, 481, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setText(QtGui.QApplication.translate("MainWindow", "A Hierarchical Directory Approach", None, QtGui.QApplication.UnicodeUTF8))
        self.TitleLabel.setObjectName(_fromUtf8("TitleLabel"))
        self.OurTeamLabel = QtGui.QLabel(self.centralwidget)
        self.OurTeamLabel.setGeometry(QtCore.QRect(170, 47, 161, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.OurTeamLabel.setFont(font)
        self.OurTeamLabel.setText(QtGui.QApplication.translate("MainWindow", "developed by FGMteam", None, QtGui.QApplication.UnicodeUTF8))
        self.OurTeamLabel.setObjectName(_fromUtf8("OurTeamLabel"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(70, 90, 371, 141))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.FeaturesLabel = QtGui.QLabel(self.frame)
        self.FeaturesLabel.setGeometry(QtCore.QRect(45, 20, 281, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.FeaturesLabel.setFont(font)
        self.FeaturesLabel.setText(QtGui.QApplication.translate("MainWindow", "select which features run", None, QtGui.QApplication.UnicodeUTF8))
        self.FeaturesLabel.setObjectName(_fromUtf8("FeaturesLabel"))
        self.Splash_SUPERnodeBtn = QtGui.QPushButton(self.frame)
        self.Splash_SUPERnodeBtn.setGeometry(QtCore.QRect(13, 90, 97, 27))
        self.Splash_SUPERnodeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Splash_SUPERnodeBtn.setText(QtGui.QApplication.translate("MainWindow", "SUPERnode", None, QtGui.QApplication.UnicodeUTF8))
        self.Splash_SUPERnodeBtn.setObjectName(_fromUtf8("Splash_SUPERnodeBtn"))
        self.Splash_nodeBtn = QtGui.QPushButton(self.frame)
        self.Splash_nodeBtn.setGeometry(QtCore.QRect(137, 90, 97, 27))
        self.Splash_nodeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Splash_nodeBtn.setText(QtGui.QApplication.translate("MainWindow", "node", None, QtGui.QApplication.UnicodeUTF8))
        self.Splash_nodeBtn.setObjectName(_fromUtf8("Splash_nodeBtn"))
        self.Splash_NothingBtn = QtGui.QPushButton(self.frame)
        self.Splash_NothingBtn.setGeometry(QtCore.QRect(260, 90, 97, 27))
        self.Splash_NothingBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Splash_NothingBtn.setText(QtGui.QApplication.translate("MainWindow", "Nothing!", None, QtGui.QApplication.UnicodeUTF8))
        self.Splash_NothingBtn.setObjectName(_fromUtf8("Splash_NothingBtn"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.Splash_statusbar = QtGui.QStatusBar(MainWindow)
        self.Splash_statusbar.setObjectName(_fromUtf8("Splash_statusbar"))
        MainWindow.setStatusBar(self.Splash_statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.Splash_SUPERnodeBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Splash_statusbar.clearMessage)
        QtCore.QObject.connect(self.Splash_nodeBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Splash_statusbar.clearMessage)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
