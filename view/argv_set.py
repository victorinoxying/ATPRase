# -*- coding: utf-8 -*-

"""
Module implementing argvDialog.
"""

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication

from view.ui.ui_argv_set import Ui_Dialog


class argvDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, argv, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(argvDialog, self).__init__(parent)
        self.setupUi(self)
        self.argv_set_le.setText(argv)

    @pyqtSlot(str)
    def on_argv_set_le_textChanged(self, text):
        """
        文字修改时，解析并显示
        """
        self.argv = text
        # self.argv_info_pte.setPlainText(self.argv)
        # 将参数原始字符串解析
        argv_list = self.argv.split(';')
        print('argv_list', argv_list)
        s_str = ''
        for i in range(len(argv_list) - 1):
            li = argv_list[i].split('_')  # 将元素解构为列表，第一位为取值方式，后续为参数值
            print(li)
            if i % 2 == 0:
                if li[0] == 's':
                    s = '闭合时间，单值%s' % li[1]
                elif li[0] == 'p':
                    s = '闭合时间，步长[%s,%s]' % (li[1], li[2])
                elif li[0] == 'u':
                    s = '闭合时间，均匀分布[%s,%s]' % (li[1], li[2])
                elif li[0] == 'n':
                    s = '闭合时间，正态分布[%s,%s]' % (li[1], li[2])
                else:
                    print('不太对')
            else:
                if li[0] == 's':
                    s = '断开时间，单值%s' % li[1]
                elif li[0] == 'p':
                    s = '断开时间，步长[%s,%s]' % (li[1], li[2])
                elif li[0] == 'u':
                    s = '断开时间，均匀分布[%s,%s]' % (li[1], li[2])
                elif li[0] == 'n':
                    s = '断开时间，正态分布[%s,%s]' % (li[1], li[2])
                else:
                    print('不太对')
            s_str += (s + '\n')

        self.argv_info_pte.setPlainText(s_str)

    @pyqtSlot()
    def on_argv_action_btn_clicked(self):
        """
        添加动作按钮
        :return:
        """
        value = self.argv_value_le.text()

        # 判断是否有值
        if not value:
            return

        self.argv = self.argv_set_le.text()

        if self.argv_cb.currentText() == '单值':
            self.argv += 's_' + self.argv_value_le.text() + ';'
        elif self.argv_cb.currentText() == '步长':
            if not '_' in self.argv_value_le.text():
                return
            self.argv += 'p_' + self.argv_value_le.text() + ';'
        elif self.argv_cb.currentText() == '均匀分布':
            if not '_' in self.argv_value_le.text():
                return
            self.argv += 'u_' + self.argv_value_le.text() + ';'
        elif self.argv_cb.currentText() == '正态分布':
            if not '_' in self.argv_value_le.text():
                return
            self.argv += 'n_' + self.argv_value_le.text() + ';'
        else:
            print('出现奇怪的异常')

        self.argv_set_le.setText(self.argv)
        self.argv_value_le.clear()

    def get_argv(self):
        if len(self.argv) > 0 and self.argv[-1] != ';':
            self.argv += ';'
        return self.argv

    @pyqtSlot()
    def on_argv_confirm_btn_clicked(self):
        """
        确认按钮
        """
        self.on_argv_action_btn_clicked()
        self.accept()

    @pyqtSlot()
    def on_argv_cancel_le_clicked(self):
        """
        取消按钮
        """
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = argvDialog('s_-1;s_2;')
    dlg.show()
    sys.exit(app.exec_())
