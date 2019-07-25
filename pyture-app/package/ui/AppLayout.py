# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/AppLayout.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 711)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imageLbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLbl.sizePolicy().hasHeightForWidth())
        self.imageLbl.setSizePolicy(sizePolicy)
        self.imageLbl.setText("")
        self.imageLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLbl.setObjectName("imageLbl")
        self.horizontalLayout.addWidget(self.imageLbl)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionSet_Timer = QtWidgets.QAction(MainWindow)
        self.actionSet_Timer.setObjectName("actionSet_Timer")
        self.actionCancel_Timer = QtWidgets.QAction(MainWindow)
        self.actionCancel_Timer.setObjectName("actionCancel_Timer")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PytureApp"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionSet_Timer.setText(_translate("MainWindow", "Set Timer"))
        self.actionCancel_Timer.setText(_translate("MainWindow", "Cancel Timer"))

