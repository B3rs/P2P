# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Apr 16 10:20:11 2012
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
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(27)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.mainTabWidget = QtGui.QTabWidget(self.centralwidget)
        self.mainTabWidget.setObjectName(_fromUtf8("mainTabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(418, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_9 = QtGui.QLabel(self.tab)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout.addWidget(self.label_9)
        self.ttlPeersSearchSpinBox = QtGui.QSpinBox(self.tab)
        self.ttlPeersSearchSpinBox.setMinimum(1)
        self.ttlPeersSearchSpinBox.setProperty("value", 3)
        self.ttlPeersSearchSpinBox.setObjectName(_fromUtf8("ttlPeersSearchSpinBox"))
        self.horizontalLayout.addWidget(self.ttlPeersSearchSpinBox)
        self.searchNeighboursBtn = QtGui.QPushButton(self.tab)
        self.searchNeighboursBtn.setObjectName(_fromUtf8("searchNeighboursBtn"))
        self.horizontalLayout.addWidget(self.searchNeighboursBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.peersTreeWidget = QtGui.QTreeWidget(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.peersTreeWidget.sizePolicy().hasHeightForWidth())
        self.peersTreeWidget.setSizePolicy(sizePolicy)
        self.peersTreeWidget.setAlternatingRowColors(True)
        self.peersTreeWidget.setItemsExpandable(False)
        self.peersTreeWidget.setObjectName(_fromUtf8("peersTreeWidget"))
        self.verticalLayout_5.addWidget(self.peersTreeWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.peerIP = QtGui.QLineEdit(self.tab)
        self.peerIP.setText(_fromUtf8(""))
        self.peerIP.setObjectName(_fromUtf8("peerIP"))
        self.horizontalLayout_2.addWidget(self.peerIP)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_2.addWidget(self.label_6)
        self.peerPort = QtGui.QLineEdit(self.tab)
        self.peerPort.setText(_fromUtf8(""))
        self.peerPort.setObjectName(_fromUtf8("peerPort"))
        self.horizontalLayout_2.addWidget(self.peerPort)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.addPeerBtn = QtGui.QPushButton(self.tab)
        self.addPeerBtn.setObjectName(_fromUtf8("addPeerBtn"))
        self.horizontalLayout_2.addWidget(self.addPeerBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.mainTabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.sharedFilesListWidget = QtGui.QListWidget(self.tab_2)
        self.sharedFilesListWidget.setAlternatingRowColors(True)
        self.sharedFilesListWidget.setObjectName(_fromUtf8("sharedFilesListWidget"))
        self.verticalLayout_4.addWidget(self.sharedFilesListWidget)
        self.mainTabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_7 = QtGui.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_3.addWidget(self.label_7)
        self.downloadsTreeWidget = QtGui.QTreeWidget(self.tab_3)
        self.downloadsTreeWidget.setAlternatingRowColors(True)
        self.downloadsTreeWidget.setObjectName(_fromUtf8("downloadsTreeWidget"))
        self.verticalLayout_3.addWidget(self.downloadsTreeWidget)
        self.label_8 = QtGui.QLabel(self.tab_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_3.addWidget(self.label_8)
        self.uploadsTreeWidget = QtGui.QTreeWidget(self.tab_3)
        self.uploadsTreeWidget.setAlternatingRowColors(True)
        self.uploadsTreeWidget.setObjectName(_fromUtf8("uploadsTreeWidget"))
        self.verticalLayout_3.addWidget(self.uploadsTreeWidget)
        self.mainTabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.tab_4)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.searchLineEdit = QtGui.QLineEdit(self.tab_4)
        self.searchLineEdit.setObjectName(_fromUtf8("searchLineEdit"))
        self.horizontalLayout_3.addWidget(self.searchLineEdit)
        self.label_10 = QtGui.QLabel(self.tab_4)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_3.addWidget(self.label_10)
        self.ttlFilesSearchSpinBox = QtGui.QSpinBox(self.tab_4)
        self.ttlFilesSearchSpinBox.setMinimum(1)
        self.ttlFilesSearchSpinBox.setProperty("value", 3)
        self.ttlFilesSearchSpinBox.setObjectName(_fromUtf8("ttlFilesSearchSpinBox"))
        self.horizontalLayout_3.addWidget(self.ttlFilesSearchSpinBox)
        self.searchBtn = QtGui.QPushButton(self.tab_4)
        self.searchBtn.setObjectName(_fromUtf8("searchBtn"))
        self.horizontalLayout_3.addWidget(self.searchBtn)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.resultsTreeWidget = QtGui.QTreeWidget(self.tab_4)
        self.resultsTreeWidget.setAlternatingRowColors(True)
        self.resultsTreeWidget.setObjectName(_fromUtf8("resultsTreeWidget"))
        self.verticalLayout_6.addWidget(self.resultsTreeWidget)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(self.tab_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        spacerItem2 = QtGui.QSpacerItem(358, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.mainTabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tab_5)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.loggingTextBrowser = QtGui.QTextBrowser(self.tab_5)
        self.loggingTextBrowser.setObjectName(_fromUtf8("loggingTextBrowser"))
        self.verticalLayout_7.addWidget(self.loggingTextBrowser)
        self.mainTabWidget.addTab(self.tab_5, _fromUtf8(""))
        self.verticalLayout.addWidget(self.mainTabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.mainTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Gnutella client", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "by Ferrari Luca, Bersani Marco, Lodi Giovanni", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "TTL:", None, QtGui.QApplication.UnicodeUTF8))
        self.searchNeighboursBtn.setText(QtGui.QApplication.translate("MainWindow", "Search neighbours", None, QtGui.QApplication.UnicodeUTF8))
        self.peersTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Peer IP", None, QtGui.QApplication.UnicodeUTF8))
        self.peersTreeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Peer Port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Peer IP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Peer port", None, QtGui.QApplication.UnicodeUTF8))
        self.addPeerBtn.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Neighbours", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Shared files", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Downloads:", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadsTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadsTreeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Percentage", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadsTreeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Peer", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadsTreeWidget.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Md5", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Uploads:", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadsTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadsTreeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Percentage", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadsTreeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Peer", None, QtGui.QApplication.UnicodeUTF8))
        self.uploadsTreeWidget.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Md5", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Transfers", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "File name to search:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "TTL:", None, QtGui.QApplication.UnicodeUTF8))
        self.searchBtn.setText(QtGui.QApplication.translate("MainWindow", "Search!", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTreeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTreeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Peer IP", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTreeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "Peer port", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsTreeWidget.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Md5", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Double click on a file to download it", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("MainWindow", "Logging", None, QtGui.QApplication.UnicodeUTF8))

