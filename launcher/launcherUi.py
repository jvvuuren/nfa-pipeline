# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launcher.ui'
#
# Created: Tue Jan 22 15:48:06 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(938, 623)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.projectListWidget = QtGui.QListWidget(self.centralwidget)
        self.projectListWidget.setObjectName("projectListWidget")
        self.horizontalLayout.addWidget(self.projectListWidget)
        self.shotListWidget = QtGui.QListWidget(self.centralwidget)
        self.shotListWidget.setObjectName("shotListWidget")
        self.horizontalLayout.addWidget(self.shotListWidget)
        self.actionGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.actionGroupBox.setObjectName("actionGroupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.actionGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.nukeButton = QtGui.QPushButton(self.actionGroupBox)
        self.nukeButton.setText("")
        self.nukeButton.setObjectName("nukeButton")
        self.verticalLayout.addWidget(self.nukeButton)
        self.mayaButton = QtGui.QPushButton(self.actionGroupBox)
        self.mayaButton.setText("")
        self.mayaButton.setObjectName("mayaButton")
        self.verticalLayout.addWidget(self.mayaButton)
        self.houdiniButton = QtGui.QPushButton(self.actionGroupBox)
        self.houdiniButton.setText("")
        self.houdiniButton.setObjectName("houdiniButton")
        self.verticalLayout.addWidget(self.houdiniButton)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.folderButton = QtGui.QPushButton(self.actionGroupBox)
        self.folderButton.setText("")
        self.folderButton.setObjectName("folderButton")
        self.verticalLayout.addWidget(self.folderButton)
        self.inputButton = QtGui.QPushButton(self.actionGroupBox)
        self.inputButton.setText("")
        self.inputButton.setObjectName("inputButton")
        self.verticalLayout.addWidget(self.inputButton)
        self.outputButton = QtGui.QPushButton(self.actionGroupBox)
        self.outputButton.setText("")
        self.outputButton.setObjectName("outputButton")
        self.verticalLayout.addWidget(self.outputButton)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.actionGroupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 938, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGroupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))

