# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import cgitb
import os
import sys
import threading
import time
import win32api
import win32gui

import win32con
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QListWidgetItem, QMessageBox, QComboBox, \
    QPushButton, QProgressDialog

from atp.CreateAtp import CreateAtp
from atp.ParseHandler import ParseHandler
from atp.RunATP import RunATP
from utils.AtpBat import AtpBat
from utils.AtpSetting import AtpSetting
from utils.Convert import Convert
from utils.UIUtils import UIUtils
from view.argv_set import argvDialog
from view.controller.SwtichController import SwitchController
from view.ui.ui_ATP_Helper import Ui_MainWindow


# todo menu中的操作，参数设置中下划线

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, file, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 初始化
        # self.switch_controller = SwitchController([self.switch_node, self.switch_arg_set, self.switch_arg_del])
        self.switch_controller = SwitchController()

        # 总界面超参数初始化
        self.total_time.setText('3')
        self.time_offset.setText(str(AtpSetting.get_time_offset()))
        self.lineEdit_3.setText('100')
        self.lineEdit_4.setText('0')
        self.lineEdit_5.setText('10')

        self.__handler = None

        self.__runAtp = RunATP()

        # 选择文件后，解析路径和文件名
        self.__adp_file = file
        self.__adp_path, self.__adp_file_name = os.path.split(file)
        self.__adp_file_name = os.path.splitext(self.__adp_file_name)[0]
        print("adpfile: path: %s, file name: %s" % (self.__adp_path, self.__adp_file_name))

        win32api.ShellExecute(0, 'open', file, '', '', 1)
        time.sleep(1)

        # 获取句柄
        self.handle_atpdraw = win32gui.FindWindow(None, u"ATPDraw")
        self.handle_myatp = win32gui.FindWindow(None, u"MainWindow")

        # 加载switch模式保存
        for name in self.switch_controller.load_model(self.__adp_file_name):
            self.switch_model_list.addItem(name)

        # 更新一下atp
        self.on_atp_update_clicked()

    def modify_ATPDRaw_size(self, x, y, width, height):
        # 修改窗口大小
        win32gui.SetWindowPos(self.handle_atpdraw, None, x, y, width, height,
                              win32con.SWP_NOSENDCHANGING | win32con.SWP_SHOWWINDOW)
        # win32gui.SetWindowPos(self.handle_myatp, None, width - 620, 0, 620, height,
        #                       win32con.SWP_NOSENDCHANGING | win32con.SWP_SHOWWINDOW)

    def loadOutput(self):
        """
        加载结果处理与分析页面的结果标签，根据atp中output加载
        :return:
        """
        # 结果处理与分析页面
        # 填入项目名称
        self.result_pro_name_le.setText(self.__atp_file)
        # 添加结果标签多选栏
        self.result_tips = self.__handler.output.output
        self.result_tips_widget = []  # 存放每个标签对应的多选框，因为是一一对应关系，所以索引相同。
        # 先清空标签
        UIUtils.deleteLayout(self.result_tips_gl)
        # 根据不同的atp文件动态添加多选栏
        for i in range(len(self.result_tips)):
            self.result_tips_cb = QtWidgets.QCheckBox(self.tab_7)
            self.result_tips_cb.setObjectName(self.result_tips[i])
            self.result_tips_cb.setText(self.result_tips[i])
            self.result_tips_widget.append(self.result_tips_cb)
            self.result_tips_gl.addWidget(self.result_tips_cb, i // 3, i % 3)

    # def refreshSwitchTag(self):
    #     """
    #     刷新开关标签
    #     :return:
    #     """
    #     # todo 删除不一致的
    #     for v in self.__handler.switch.values():
    #         self.switch_node.addItem(v.getNodes())

    @pyqtSlot()
    def on_set_runATP_clicked(self):
        """
        设置runatp的路径
        :return:
        """
        file, n_1 = QFileDialog.getOpenFileName(self, "请选取runATP_G.bat脚本文件", '', 'BAT(*.bat)')
        # 没有选择文件
        if not file:
            return
        AtpBat.modify_bat(file)

    @pyqtSlot()
    def on_load_adp_btn_clicked(self):
        """
        加载adp按钮
        打开atpdraw，并调整窗口大小
        :return:
        """
        # 获取文件名
        file, n_1 = QFileDialog.getOpenFileName(self, "选取项目文件", '', 'ADP or ACP Files(*.adp *.acp)')
        # 没有选择文件
        if not file:
            return

        # 选择文件后，解析路径和文件名
        self.__adp_file = file
        self.__adp_path, self.__adp_file_name = os.path.split(file)
        self.__adp_file_name = os.path.splitext(self.__adp_file_name)[0]
        print("adpfile: path: %s, file name: %s" % (self.__adp_path, self.__adp_file_name))

        win32api.ShellExecute(0, 'open', file, '', '', 1)
        time.sleep(1)

        # 获取句柄
        self.handle_atpdraw = win32gui.FindWindow(None, u"ATPDraw")
        self.handle_myatp = win32gui.FindWindow(None, u"MainWindow")

        # 获得当前工作屏幕长宽
        work_area = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0))).get("Work")
        width = work_area[2]
        height = work_area[3]
        print("width =", width)
        print("height =", height)

        # 修改窗口大小
        win32gui.SetWindowPos(self.handle_atpdraw, None, 0, 0, width - 620, height,
                              win32con.SWP_NOSENDCHANGING | win32con.SWP_SHOWWINDOW)
        win32gui.SetWindowPos(self.handle_myatp, None, width - 620, 0, 620, height,
                              win32con.SWP_NOSENDCHANGING | win32con.SWP_SHOWWINDOW)

        # 更新一下atp
        self.on_atp_update_clicked()

    # @pyqtSlot()
    # def on_load_atp_btn_clicked(self):
    #     """
    #     加载atp项目按钮
    #     加载并解析atp文件，做一些初始化工作
    #     :return:
    #     """
    #     # 获取文件名
    #     file, n_1 = QFileDialog.getOpenFileName(self, "选取文件", '', 'Text Files(*.atp)')
    #     # 没有选择文件
    #     if not file:
    #         return
    #
    #     # 选择文件后，解析路径和文件名
    #     self.__atp_file = file
    #     self.__atp_path, self.__atp_file_name = os.path.split(file)
    #     self.__atp_file_name = os.path.splitext(self.__atp_file_name)[0]
    #     print("atpfile: path: %s, file name: %s" % (self.__atp_path, self.__atp_file_name))
    #
    #     self.__adp_path = self.__atp_path
    #     self.__adp_file_name = self.__atp_file_name
    #
    #     self.parse_atp(self.__atp_file)

    def parse_atp(self, path):
        """
        解析atp文件
        :param path:
        :return:
        """
        # 开始解析
        self.__handler = ParseHandler()
        self.__handler.parse(path)

        # ————————————————————————
        # 根据读入的项目信息对结果页面进行相应的调整
        # ————————————————————————
        # 加载output标签
        self.loadOutput()

        # 警报不一致项
        compare = self.switch_controller.compare_argset(list(self.__handler.switch.keys()))
        if len(compare) > 0:
            QMessageBox.warning(self, "错误", "以下结点与模式不匹配,已被删除：\n%s" % ''.join(compare))
            self.switch_controller.remove_list(compare)

    @pyqtSlot()
    def on_atp_update_clicked(self):
        """
        更新按钮
        :return:
        """
        print("on_atp_refresh_clicked")
        # 修改配置文件内容
        AtpBat.setAtpConf('0')
        time.sleep(1)
        # 发送F2键
        win32api.PostMessage(self.handle_atpdraw, win32con.WM_KEYDOWN, win32con.VK_F2, 0)

        # 等待atp生成
        time.sleep(2)

        # 更新atp路径
        path = AtpBat.getAtpPath()
        self.__atp_file = path

        self.parse_atp(self.__atp_file)

    @pyqtSlot()
    def on_atp_run_clicked(self):
        """
        运行按钮
        :return:
        """
        print('on_atp_run_clicked')

        # 先更新atp
        # 更新路径，对比不一致项
        self.on_atp_update_clicked()

        # 修改配置文件
        AtpBat.setAtpConf('1')
        time.sleep(1)
        # 发送F2键
        win32api.PostMessage(self.handle_atpdraw, win32con.WM_KEYDOWN, win32con.VK_F2, 0)

        # 等待atp生成
        # time.sleep(1)

        # # 更新atp路径
        # path = UpdateAtp.getPathConf()
        # fname, fextension = os.path.splitext(path)
        # self.__atp_file = os.path.join(self.__adp_path, fname + '.atp')
        # self.__atp_path = self.__adp_path
        #
        # self.parse_atp(self.__atp_file)

        # 警报不一致项
        # compare = self.switch_controller.compare_model(self.__handler.switch.keys())
        # if len(compare) > 0:
        #     QMessageBox.warning(self, "错误", "以下结点与模式不匹配：\n%s" % ''.join(compare))

    ####################  开关页面  #############################

    @pyqtSlot(str)
    def on_switch_node_currentIndexChanged(self, text):
        print("on_switch_node_currentIndexChanged: " + text)

        if not self.__handler:
            return

        # 先遍历找到该组组件
        widgetIndex = 0
        for i in self.switch_controller.get_widget_list():
            try:
                i.index(self.sender())
                break
            except:
                pass
            widgetIndex += 1

        # 修改结点
        self.switch_controller.switch_arg_set_list.setEntity(text, widgetIndex)

    @pyqtSlot()
    def on_switch_arg_set_clicked(self):
        """
        开关参数设置按钮
        :return:
        """
        print("on_switch_arg_set_clicked")

        if not self.__handler:
            return

        # 先遍历找到该组组件
        widgetIndex = 0
        for i in self.switch_controller.get_widget_list():
            try:
                i.index(self.sender())
                break
            except:
                pass
            widgetIndex += 1

        print("switch arg set index: %d" % widgetIndex)

        # 找到设置的参数，打开设置界面
        ui = argvDialog(self.switch_controller.switch_arg_set_clicked(self.__handler.switch, widgetIndex),
                        parent=self)
        # ui = argvDialog('s_-1;s_2;', parent=self)
        ui.show()
        if ui.exec_():
            print("ui.get_argv: " + ui.get_argv())
            self.switch_controller.setArg(ui.get_argv(), widgetIndex)
            print(self.switch_controller.get_arg_list())

    @pyqtSlot()
    def on_switch_arg_del_clicked(self):
        """
        删除指定参数
        :return:
        """
        print("on_switch_arg_del_clicked")

        # 如果没有加载atp，则不能删除
        if len(self.__atp_file) <= 0:
            return

        # 先遍历找到该组组件
        widgetIndex = 0
        for i in self.switch_controller.get_widget_list():
            try:
                i.index(self.sender())
                break
            except:
                pass
            widgetIndex += 1

        # 删除
        for widget in self.switch_controller.get_widget_list()[widgetIndex]:
            widget.deleteLater()
            del widget

        self.switch_controller.switch_arg_del_clicked(widgetIndex)

        print('current switch arg list: ')
        print(self.switch_controller.switch_arg_set_list.argList)

    @pyqtSlot()
    def on_switch_add_list_clicked(self):
        """
        添加新一组开关模式
        :return:
        """
        print("on_switch_add_list_clicked")
        # 如果没有加载atp，则不能添加
        if len(self.__atp_file) <= 0:
            return

        row = self.gridLayout_2.rowCount()

        widgets = self.create_switch_ui(row, self.__handler.switch)

        self.gridLayout_2.addWidget(widgets[0], row, 0)
        self.gridLayout_2.addWidget(widgets[1], row, 1)
        self.gridLayout_2.addWidget(widgets[2], row, 2)

    @pyqtSlot()
    def on_switch_model_save_clicked(self):
        """
        模式保存按钮
        :return:
        """
        # 如果没有加载atp，则不能保存
        if len(self.__atp_file) <= 0:
            return

        name = self.switch_model_name.text()
        print("model name:" + name)

        if (len(name) <= 0):
            QMessageBox.warning(self, "错误", "模式名不能为空")
            return

        # 保存并修改ui
        if not self.switch_controller.model_save(name):
            self.switch_model_list.addItem(name)

    @pyqtSlot()
    def on_switch_model_apply_clicked(self):
        """
        模式应用按钮
        :return:
        """
        # 如果没有加载atp，则不能应用
        if len(self.__atp_file) <= 0:
            return

        UIUtils.deleteLayout(self.gridLayout_2)

        name = self.switch_model_list.currentItem().text()

        widget_list = self.switch_controller.switch_model_apply_cliced(name, self.create_switch_ui,
                                                                       self.__handler.switch)
        for i in range(len(widget_list)):
            self.gridLayout_2.addWidget(widget_list[i][0], i, 0)
            self.gridLayout_2.addWidget(widget_list[i][1], i, 1)
            self.gridLayout_2.addWidget(widget_list[i][2], i, 2)

        # 警报不一致项
        compare = self.switch_controller.compare_model_argset(list(self.__handler.switch.keys()), name)
        if len(compare) > 0:
            QMessageBox.warning(self, "错误", "以下结点与模式不匹配,已被删除：\n%s" % ''.join(compare))
            self.switch_controller.remove_list(compare)

    @pyqtSlot()
    def on_switch_model_del_clicked(self):
        """
        删除模式
        :return:
        """
        print("on_switch_model_del_clicked")

        # 如果没有加载atp，则不能删除
        if len(self.__atp_file) <= 0:
            return

        # 获取模式名，删除
        row = self.switch_model_list.currentRow()
        item = self.switch_model_list.takeItem(row)
        name = item.text()
        self.switch_controller.switch_model_del_clicked(name)
        self.switch_model_info.clear()

    @pyqtSlot(QListWidgetItem)
    def on_switch_model_list_itemClicked(self, item):
        """
        展示点击的模式信息
        :param item:
        :return:
        """
        print("on_switch_model_list_itemClicked " + item.text())

        arglist = self.switch_controller.switch_model_list_itemClicked(item.text())
        self.switch_model_info.clear()

        for list in arglist:
            self.switch_model_info.append(" ".join(str(i) for i in list))

    def create_switch_ui(self, row, nodes):
        """
        创建新一行的ui控件
        :return:
        """
        switch_cm = QComboBox(self.scrollAreaWidgetContents_2)
        switch_cm.setObjectName("switch_node_%d" % row)

        switch_arg_set = QPushButton(self.scrollAreaWidgetContents_2)
        switch_arg_set.setObjectName("switch_arg_set_%d" % row)

        switch_arg_del = QPushButton(self.scrollAreaWidgetContents_2)
        switch_arg_del.setObjectName("switch_arg_del_%d" % row)

        switch_arg_set.setText("参数设置")
        switch_arg_del.setText("移除")

        # 添加结点组
        for i in nodes:
            switch_cm.addItem(i)

        self.switch_controller.append_widget([switch_cm, switch_arg_set, switch_arg_del])

        # 一定要把这几个方法放到添加了数组之后
        switch_cm.currentTextChanged.connect(self.on_switch_node_currentIndexChanged)
        switch_arg_set.clicked.connect(self.on_switch_arg_set_clicked)
        switch_arg_del.clicked.connect(self.on_switch_arg_del_clicked)

        print('create new switch ui')

        return [switch_cm, switch_arg_set, switch_arg_del]

    ################################### 结果页面 #######################################
    @pyqtSlot()
    def on_result_all_cb_checked(self):
        """
        结果页面仿真结果全选
        """
        if self.result_all_cb.isChecked():
            self.result_max_cb.setChecked(True)
            self.result_min_cb.setChecked(True)
            self.result_average_cb.setChecked(True)
        else:
            pass

    @pyqtSlot()
    def on_result_all_tips_rB_toggled(self, value):
        """
        结果页面结果标签全选
        :param self:
        :return:
        """
        print("on_result_all_tips_rB_clicked")
        try:
            if self.result_all_tips_rB.isChecked():
                for i in range(len(self.result_tips)):
                    self.result_tips_widget[i].setChecked(True)
            else:
                for i in range(len(self.result_tips)):
                    self.result_tips_widget[i].setChecked(False)
        except:
            pass

    ############################# 项目参数选项 ##############################

    @pyqtSlot()
    def on_time_offset_editingFinished(self):
        print('editing time offset: ' + self.time_offset.text())
        AtpSetting.set_time_offset(Convert.toDecimal(self.time_offset.text()))

    ##############################  运行 ##################################

    @pyqtSlot()
    def on_btn_run_clicked(self):
        print("on_btn_run_clicked")

        # 进度条
        self.progress = QProgressDialog(self)
        self.progress.setWindowTitle("请稍等")
        self.progress.setLabelText("正在运行...")
        self.progress.setCancelButtonText('隐藏')
        self.progress.setRange(0, 100)

        # 获取选择的结果标签
        output = []
        for i in range(len(self.result_tips)):
            if self.result_tips_widget[i].isChecked():
                output.append(self.result_tips[i])

        # 获取选择的数据标签
        value = []
        if self.result_max_cb.isChecked():
            value.append('max')
        if self.result_min_cb.isChecked():
            value.append('min')
        if self.result_average_cb.isChecked():
            value.append('ave')

        # 获取时间区间
        start = self.result_start_time.text()
        end = self.result_end_time.text()

        # 如果参数不够，则弹出警告框
        if not (len(output) > 0 and len(value) > 0 and start and end):
            QMessageBox.warning(self, "错误", "输出参数设置不正确", QMessageBox.Ok | QMessageBox.Cancel)
            print("输出参数设置不正确")
            return

        # 生成字典
        # dic = [True, 0, 0.003, ['XSA', 'XSB'], ['max', 'min', 'ave']]
        dic = {'start': start, 'end': end, 'output': output, 'value': value}

        # 开始执行
        # 更新atp获取atp生成路径
        self.on_atp_update_clicked()
        # 先生成atp文件
        createAtp = CreateAtp(self.__adp_path, self.__adp_file_name, self.__handler)
        print('total count: ' + self.total_time.text())
        createAtp.create(int(self.total_time.text()), {"switch": self.switch_controller.switch_arg_set_list})

        # 找到对应的生成的目录，运行atp文件，并分析pl4，然后输出
        # 提交任务
        for i in range(int(self.total_time.text())):
            path = '%s/%s_%d' % (self.__adp_path, self.__adp_file_name, i)
            print(path)
            self.__runAtp.submit(path, self.__adp_file_name, dic)
        # 更新进度条的信号槽
        self.__runAtp.progressUpdated.connect(self.progressbar_change)
        # 开始运行
        self.__runAtp.start()

    @pyqtSlot(int)
    def progressbar_change(self, val):
        print('progress: ' + str(val))
        self.progress.setValue(val)

    def progress_timer(self, runAtp, progress):
        # print('renew progress timer!')
        ratio = runAtp.getRatio()
        if ratio != 100:
            progress.setValue(ratio)
            timer = threading.Timer(5, self.progress_timer, (runAtp, progress))
            timer.start()
        else:
            print('progress end')
            progress.setValue(100)


if __name__ == '__main__':
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # app.exec_()
    sys.exit(app.exec_())
