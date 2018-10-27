import sys
import win32api

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from view.MainWindow import MainWindow
from view.ui.ui_mainMenubar import Ui_ATPMainWindow
from utils.RecentItemRW import RecentItemRW

class MenuBar(QMainWindow, Ui_ATPMainWindow):
    def __init__(self, filePath):
        #   窗体创建
        super(MenuBar, self).__init__()
        self.setupUi(self)
        self.mainWindow = None
        self.ADP_filePath = filePath
        work_area = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0))).get("Work")
        self.monitor_width = work_area[2] - 20
        self.monitor_height = work_area[3]
        # self.setGeometry(0, 0, self.monitor_width, 25)
        self.resize(self.monitor_width, 25)
        self.move(0, 0)
        # mainWindow是否被打开
        self.is_mainWindow_showed = False
        # 菜单栏事件
        self.actionupdateATP.triggered.connect(self.updateATP)
        self.actionrunATP.triggered.connect(self.runATP)
        self.actionloadADP.triggered.connect(self.load_new_project)

    def load_new_project(self):
        file = QFileDialog.getOpenFileName(self, "选取项目文件", '', 'ADP or ACP Files(*.adp *.acp)')
        if not file:
            return
        path = str(file[0])

        # 选中后
        if path:
            # 处理存储最近项目的txt文件
            item_list = RecentItemRW.read_recent_items()
            count = len(item_list)
            if count == 0:
                item_list.append(path)
            else:
                if item_list[count - 1] != path:
                    if count == 6:
                        del item_list[0]
                        item_list.append(path)

            button = QMessageBox.question(self, "Question",
                                          self.tr("是否打开新项目替代当前项目（选择Cancel新建窗口)"),
                                          QMessageBox.Ok | QMessageBox.Cancel,
                                          QMessageBox.Ok)
            if button == QMessageBox.Ok:
                # 接口 刷新当前界面
                self.mainWindow.loadProject(path)
                # 调整ATPdraw大小
                self.showATPdraw()
            elif button == QMessageBox.Cancel:
                self.newItem_menuBar = MenuBar(path)
                self.newItem_menuBar.show()
                self.newItem_menuBar.showMainWindow()
                self.newItem_menuBar.showATPdraw()

    # 调用mainwindow的runAtp函数
    def runATP(self):
        if self.mainWindow:
            self.mainWindow.on_atp_run_clicked()

    # 调用mainwindow的updateAtp函数
    def updateATP(self):
        if self.mainWindow:
            self.mainWindow.on_atp_update_clicked()

    def showMainWindow(self):
        if not self.is_mainWindow_showed and self.ADP_filePath:
            self.mainWindow = MainWindow(self.ADP_filePath)
            leftEdge = self.monitor_width - 640
            topEdge = self.frameGeometry().y() + self.frameGeometry().height()
            width = 640
            height = self.monitor_height - self.geometry().height() - 45
            self.mainWindow.setGeometry(leftEdge, topEdge, width, height)
            self.mainWindow.setWindowFlags(Qt.FramelessWindowHint)
            self.mainWindow.show()
            self.is_mainWindow_showed = True

    def showATPdraw(self):
        topEdge = int(self.geometry().y() + self.geometry().height() + 5) + 4
        leftEdge = 0
        width = int(self.monitor_width - 640)
        height = int(self.monitor_height - self.geometry().height() - 45)
        # 需要一个接口来控制atpdraw的位置大小
        self.mainWindow.modify_ATPDRaw_size(leftEdge, topEdge, width, height)

    def closeEvent(self, *args, **kwargs):
        if self.is_mainWindow_showed:
            self.mainWindow.close()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MenuBar()
    menu.show()
    sys.exit(app.exec_())
