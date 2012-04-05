# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Apr  5 18:43:24 2012
#      by: PyQt4 UI code generator 4.9.1
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
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(27)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 40, 291, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 90, 611, 361))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.peersTreeWidget = QtGui.QTreeWidget(self.tab)
        self.peersTreeWidget.setGeometry(QtCore.QRect(10, 60, 561, 231))
        self.peersTreeWidget.setObjectName(_fromUtf8("peersTreeWidget"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.sharedFilesListWidget = QtGui.QListWidget(self.tab_2)
        self.sharedFilesListWidget.setGeometry(QtCore.QRect(10, 20, 581, 301))
        self.sharedFilesListWidget.setObjectName(_fromUtf8("sharedFilesListWidget"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.label_3 = QtGui.QLabel(self.tab_4)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 131, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.searchLineEdit = QtGui.QLineEdit(self.tab_4)
        self.searchLineEdit.setGeometry(QtCore.QRect(160, 20, 321, 22))
        self.searchLineEdit.setObjectName(_fromUtf8("searchLineEdit"))
        self.searchBtn = QtGui.QPushButton(self.tab_4)
        self.searchBtn.setGeometry(QtCore.QRect(490, 20, 101, 21))
        self.searchBtn.setObjectName(_fromUtf8("searchBtn"))
        self.resultsTreeWidget = QtGui.QTreeWidget(self.tab_4)
        self.resultsTreeWidget.setGeometry(QtCore.QRect(10, 70, 581, 231))
        self.resultsTreeWidget.setObjectName(_fromUtf8("resultsTreeWidget"))
        self.label_4 = QtGui.QLabel(self.tab_4)
        self.label_4.setGeometry(QtCore.QRect(10, 300, 241, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Gnutella client", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "by Ferrari Luca, Lodi Giovanni, Bersani Marco", None, QtGui.QApplication.UnicodeUTF8))
        self.peersTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Peer IP", None, QtGui.QApplication.UnicodeUTF8))
        self.peersTreeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Peer Port", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Neighbours", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Shared files", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Downloads", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "File name to search:", None, QtGui.QApplication.UnicodeUTF8))
        self.searchBtn.setText(QtGui.QApplication.translate("MainWindow", "Search!", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTreeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Peer IP", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTreeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Peer Port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Double click on a file to download it", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))

