# -*- coding: utf-8 -*-

"""
Module implementing resistDialog.
"""
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication

from view.ui.ui_resist_argv_set import Ui_Dialog


class resistDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, argv, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(resistDialog, self).__init__(parent)
        self.setupUi(self)
        ar = argv.split(';')

    @pyqtSlot()
    def on_radioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.lineEdit.setEnabled(True)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_5.setEnabled(False)

    @pyqtSlot()
    def on_radioButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_3.setEnabled(True)
        self.lineEdit_4.setEnabled(True)
        self.lineEdit_5.setEnabled(True)

    def get_argv(self):
        if self.argv[-1] != ';': self.argv += ';'
        return self.argv

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.accept()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = resistDialog('r1;s_12;')  # 'r3;s_1;s_3;p_1_10;p_2_12;'
    dlg.show()
    sys.exit(app.exec_())
