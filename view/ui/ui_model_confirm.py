# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'model_confirm.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_model_confirm_Dialog(object):
    def setupUi(self, model_confirm_Dialog):
        model_confirm_Dialog.setObjectName("model_confirm_Dialog")
        model_confirm_Dialog.resize(440, 218)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(model_confirm_Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.model_confirm_label = QtWidgets.QLabel(model_confirm_Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.model_confirm_label.setFont(font)
        self.model_confirm_label.setObjectName("model_confirm_label")
        self.verticalLayout.addWidget(self.model_confirm_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.model_confirm_confirm = QtWidgets.QPushButton(model_confirm_Dialog)
        self.model_confirm_confirm.setObjectName("model_confirm_confirm")
        self.horizontalLayout.addWidget(self.model_confirm_confirm)
        self.model_confirm_cancel = QtWidgets.QPushButton(model_confirm_Dialog)
        self.model_confirm_cancel.setObjectName("model_confirm_cancel")
        self.horizontalLayout.addWidget(self.model_confirm_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(model_confirm_Dialog)
        QtCore.QMetaObject.connectSlotsByName(model_confirm_Dialog)

    def retranslateUi(self, model_confirm_Dialog):
        _translate = QtCore.QCoreApplication.translate
        model_confirm_Dialog.setWindowTitle(_translate("model_confirm_Dialog", "模式确认"))
        self.model_confirm_label.setText(_translate("model_confirm_Dialog", "是否启用？"))
        self.model_confirm_confirm.setText(_translate("model_confirm_Dialog", "确认"))
        self.model_confirm_cancel.setText(_translate("model_confirm_Dialog", "取消"))

