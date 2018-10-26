import cgitb
import os
import sys

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox

from utils.AtpBat import AtpBat
from view.MenuBarTest import MenuBar
from view.ui.ui_Welcom import Ui_WelcomeWindow


class WelcomWindow(QMainWindow, Ui_WelcomeWindow):
    def __init__(self):
        super(WelcomWindow, self).__init__()
        self.setupUi(self)
        self.menuBar = None
        self.__recent_items_path = 'data\\recent_use_item.txt'
        self.recent_item_list = []
        self.reset_recent_item_label()

        #   需要一个 打开文件夹 调用adp的接口
        self.button_loadADP.clicked.connect(self.load_ADPfile)
        self.button_settingATPRun.clicked.connect(self.setting_runATPexe)

        if not os.path.exists('data'):
            os.mkdir('data')

    #   设置runATp 的路径函数
    #   待完成
    def setting_runATPexe(self):
        file, n_1 = QFileDialog.getOpenFileName(self, "请选取runATP_G.bat脚本文件", '', 'BAT(*.bat)')
        if not file:
            return
        #   设置apt路径接口
        AtpBat.modify_bat(file)

    def __get_name(self, path):
        index_start = path.rfind('/')
        index_end = path.rfind('.')
        name = path[index_start + 1: index_end]
        return name

    # 加载adp文件
    def load_ADPfile(self):
        # 先配置脚本
        if not AtpBat.isBatExists():
            QMessageBox.warning(self, "错误", '请先配置runATP_G.bat脚本文件')
            return

        file = QFileDialog.getOpenFileName(self, "选取项目文件", '', 'ADP or ACP Files(*.adp *.acp)')

        if not file:
            return
        path = str(file[0])

        # 选中后
        if path:
            # 处理存储最近项目的txt文件
            count = self.read_recent_items()
            if count == 0:
                self.recent_item_list.append(path)
            else:
                if self.recent_item_list[count - 1] != path:
                    if count == 6:
                        del self.recent_item_list[0]
                    self.recent_item_list.append(path)

            self.write_recent_items()
            #   接口，将file传递给menu->mainwindow
            self.show_MenuBar_MainWindow(path)

    # 添加相最近打开项目的label到主界面
    def reset_recent_item_label(self):
        count = self.read_recent_items()
        self.label_1.setText("")
        self.label_1.setFilePath(None)
        self.label_2.setText("")
        self.label_2.setFilePath(None)
        self.label_3.setText("")
        self.label_3.setFilePath(None)
        self.label_4.setText("")
        self.label_4.setFilePath(None)
        self.label_5.setText("")
        self.label_5.setFilePath(None)
        self.label_6.setText("")
        self.label_6.setFilePath(None)
        if count == 0:
            return
        else:
            count -= 1
            self.label_1.setText(self.__get_name(self.recent_item_list[count]) + '\n' + self.recent_item_list[count])
            self.label_1.setFilePath(self.recent_item_list[count])
            self.label_1.clicked.connect(self.label1_clicked)
            if count == 0:
                return

            count -= 1
            self.label_2.setText(self.__get_name(self.recent_item_list[count]) + '\n' + self.recent_item_list[count])
            self.label_2.setFilePath(self.recent_item_list[count])
            self.label_2.clicked.connect(self.label2_clicked)
            if count == 0:
                return

            count -= 1
            self.label_3.setText(self.__get_name(self.recent_item_list[count]) + '\n' + self.recent_item_list[count])
            self.label_3.setFilePath(self.recent_item_list[count])
            self.label_3.clicked.connect(self.label3_clicked)
            if count == 0:
                return

            count -= 1
            self.label_4.setText(self.__get_name(self.recent_item_list[count]) + '\n' + self.recent_item_list[count])
            self.label_4.setFilePath(self.recent_item_list[count])
            self.label_4.clicked.connect(self.label4_clicked)
            if count == 0:
                return

            count -= 1
            self.label_5.setText(self.__get_name(self.recent_item_list[count]) + '\n' + self.recent_item_list[count])
            self.label_5.setFilePath(self.recent_item_list[count])
            self.label_5.clicked.connect(self.label5_clicked)
            if count == 0:
                return

            count -= 1
            self.label_6.setText(self.__get_name(self.recent_item_list[count]) + '\n' + self.recent_item_list[count])
            self.label_6.setFilePath(self.recent_item_list[count])
            self.label_6.clicked.connect(self.label6_clicked)
            if count == 0:
                return

    def label1_clicked(self):
        path = self.label_1.getFilePath()
        if path:
            self.show_MenuBar_MainWindow(path)

    def label2_clicked(self):
        path = self.label_2.getFilePath()
        if path:
            self.show_MenuBar_MainWindow(path)
    def label3_clicked(self):
        path = self.label_3.getFilePath()
        if path:
            self.show_MenuBar_MainWindow(path)


    def label4_clicked(self):
        path = self.label_4.getFilePath()
        if path:
            self.show_MenuBar_MainWindow(path)


    def label5_clicked(self):
        path = self.label_5.getFilePath()
        if path:
            self.show_MenuBar_MainWindow(path)


    def label6_clicked(self):
        path = self.label_6.getFilePath()
        if path:
            self.show_MenuBar_MainWindow(path)


    # 打开工作界面
    def show_MenuBar_MainWindow(self, path):
        if os.path.exists(path):
            self.menuBar = MenuBar(path)
            print(path)
            self.menuBar.show()
            self.menuBar.showMainWindow()
            self.menuBar.showATPdraw()
            self.hide()
        else:
            button = QMessageBox.question(self, "Question",
                                          self.tr("项目路径 "+path+" 已失效，是否移除？"),
                                          QMessageBox.Ok | QMessageBox.Cancel,
                                          QMessageBox.Ok)
            if button == QMessageBox.Ok:
                self.recent_item_list.remove(path)
                self.write_recent_items()
                # 刷新页面
                self.reset_recent_item_label()
            elif button == QMessageBox.Cancel:
                return



    def read_recent_items(self):
        self.recent_item_list.clear()
        if not os.path.exists(self.__recent_items_path):
            return len(self.recent_item_list)

        fileStream = open(self.__recent_items_path, 'r')
        for line in fileStream.readlines():
            if line == '\n':
                continue
            itemInfo = line.split(' ')
            self.recent_item_list.append(itemInfo[1])
        fileStream.close()
        return len(self.recent_item_list)

    def write_recent_items(self):
        fileStream = open(self.__recent_items_path, 'w+')
        for i in range(len(self.recent_item_list)):
            if i == 0:
                fileStream.write(str(i) + ' ' + self.recent_item_list[i])
            else:
                fileStream.write('\n' + str(i) + ' ' + self.recent_item_list[i])
        fileStream.close()


if __name__ == '__main__':
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    welcom = WelcomWindow()
    welcom.show()
    # app.exec_()
    sys.exit(app.exec_())
