import sys
import win32api

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from view.MainWindow import MainWindow
from view.ui.ui_mainMenubar import Ui_ATPMainWindow


class MenuBar(QMainWindow, Ui_ATPMainWindow):
    def __init__(self, filePath):
        #   窗体创建
        super(MenuBar, self).__init__()
        self.setupUi(self)
        self.ADP_filePath = filePath
        work_area = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0))).get("Work")
        self.monitor_width = work_area[2] - 20
        self.monitor_height = work_area[3]
        # self.setGeometry(0, 0, self.monitor_width, 25)
        self.resize(self.monitor_width, 25)
        self.move(0, 0)
        self.is_mainWindow_showed = False
        self.actionrunATP.triggered.connect(self.showMainWindow)
        self.actiondrawATP.triggered.connect(self.showATPdraw)

    def showMainWindow(self):
        if not self.is_mainWindow_showed and self.ADP_filePath:
            # self.mainWindow = MainWindow()
            # 修改为：
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
