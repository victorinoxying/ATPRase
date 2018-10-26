# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainMenubar.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ATPMainWindow(object):
    def setupUi(self, ATPMainWindow):
        ATPMainWindow.setObjectName("ATPMainWindow")
        ATPMainWindow.setWindowModality(QtCore.Qt.NonModal)
        ATPMainWindow.resize(961, 25)
        ATPMainWindow.setMinimumSize(QtCore.QSize(540, 25))
        ATPMainWindow.setMaximumSize(QtCore.QSize(16777215, 48))
        ATPMainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(ATPMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        ATPMainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(ATPMainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 961, 26))
        self.menuBar.setObjectName("menuBar")
        self.startMenu = QtWidgets.QMenu(self.menuBar)
        self.startMenu.setObjectName("startMenu")
        self.drawMenu = QtWidgets.QMenu(self.menuBar)
        self.drawMenu.setObjectName("drawMenu")
        self.settingMenu = QtWidgets.QMenu(self.menuBar)
        self.settingMenu.setObjectName("settingMenu")
        ATPMainWindow.setMenuBar(self.menuBar)
        self.actionloadATP = QtWidgets.QAction(ATPMainWindow)
        self.actionloadATP.setObjectName("actionloadATP")
        self.actionupdateATP = QtWidgets.QAction(ATPMainWindow)
        self.actionupdateATP.setObjectName("actionupdateATP")
        self.actionloadADP = QtWidgets.QAction(ATPMainWindow)
        self.actionloadADP.setObjectName("actionloadADP")
        self.actionrunATP = QtWidgets.QAction(ATPMainWindow)
        self.actionrunATP.setObjectName("actionrunATP")
        self.actionsetScript = QtWidgets.QAction(ATPMainWindow)
        self.actionsetScript.setObjectName("actionsetScript")
        self.actiondrawATP = QtWidgets.QAction(ATPMainWindow)
        self.actiondrawATP.setObjectName("actiondrawATP")
        self.actionnetWork = QtWidgets.QAction(ATPMainWindow)
        self.actionnetWork.setObjectName("actionnetWork")
        self.startMenu.addAction(self.actionloadATP)
        self.startMenu.addAction(self.actionloadADP)
        self.startMenu.addAction(self.actionupdateATP)
        self.startMenu.addAction(self.actionrunATP)
        self.startMenu.addAction(self.actionsetScript)
        self.drawMenu.addAction(self.actiondrawATP)
        self.settingMenu.addAction(self.actionnetWork)
        self.menuBar.addAction(self.startMenu.menuAction())
        self.menuBar.addAction(self.drawMenu.menuAction())
        self.menuBar.addAction(self.settingMenu.menuAction())

        self.retranslateUi(ATPMainWindow)
        QtCore.QMetaObject.connectSlotsByName(ATPMainWindow)

    def retranslateUi(self, ATPMainWindow):
        _translate = QtCore.QCoreApplication.translate
        ATPMainWindow.setWindowTitle(_translate("ATPMainWindow", "ATPrase"))
        self.startMenu.setTitle(_translate("ATPMainWindow", "开始"))
        self.drawMenu.setTitle(_translate("ATPMainWindow", "设计"))
        self.settingMenu.setTitle(_translate("ATPMainWindow", "设置"))
        self.actionloadATP.setText(_translate("ATPMainWindow", "加载ATP"))
        self.actionupdateATP.setText(_translate("ATPMainWindow", "更新ATP"))
        self.actionloadADP.setText(_translate("ATPMainWindow", "加载ADP"))
        self.actionrunATP.setText(_translate("ATPMainWindow", "运行项目"))
        self.actionsetScript.setText(_translate("ATPMainWindow", "设置脚本"))
        self.actiondrawATP.setText(_translate("ATPMainWindow", "设计电路图"))
        self.actionnetWork.setText(_translate("ATPMainWindow", "网络设置"))

