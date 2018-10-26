#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/22
# @Author  : RoyYoung

"""
mainwindow中，控制switch的主要行为
"""
import os

from utils.ArgvSet import ArgvSet
from utils.Model import Model


class SwitchController(object):

    def __init__(self):
        # 参数设置的工具类
        self.switch_arg_set_list = ArgvSet()

        # todo: 有控件时清空控件
        # 一行3个控件为一组，用数组记录
        self.switch_widget_list = []

        # 模式保存
        self.model = Model()
        if not os.path.exists("model"):
            os.mkdir("model")
        # 针对不同文件，会有不同的路径
        self.model_path = ''

    def load_model(self, fileName):
        """
        读取模式保存switch
        :return: 所有模式名
        """
        self.model_path = 'model/switch/' + fileName + '/'

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
            return []

        model_list = []
        files = os.listdir(self.model_path)
        for file in files:
            name = os.path.basename(file)
            model_list.append(name.rstrip("_Model_Info.txt"))

        return model_list

    def switch_arg_set_clicked(self, switch, widgetIndex):
        """
        开关参数设置按钮被按下
        设置一个参数，并返回其参数值
        :param swtich:
        :param widgetIndex:
        :return: 返回参数值
        """
        arg = self.switch_widget_list[widgetIndex][0].currentText()
        self.switch_arg_set_list.setEntity(switch[arg].getNodes(), widgetIndex)
        return self.switch_arg_set_list.getArg(widgetIndex)

    def setArg(self, arg, index):
        """
        设置一个参数的参数值
        :param arg:
        :param index:
        :return:
        """
        self.switch_arg_set_list.setArg(arg, index)

    def switch_arg_del_clicked(self, index):
        """
        参数删除按钮按下
        删除控件和参数
        :return:
        """
        self.switch_widget_list.pop(index)
        self.switch_arg_set_list.delItem(index)

    def get_arg_list(self):
        """
        获取所有参数列表
        :return:
        """
        return self.switch_arg_set_list.argList;

    def get_widget_list(self):
        """
        获取所有控件列表
        :return:
        """
        return self.switch_widget_list

    def append_widget(self, widgets):
        # 添加后，将添加的控件加入控件列表中，方便寻找sender
        self.switch_widget_list.append(widgets)
        # 添加相应的参数
        self.switch_arg_set_list.add()

    def model_save(self, model_name):
        """
        模式保存按钮
        :return: 返回文件是否存在
        """
        exists = True

        # 保存到文件
        self.model.saveSwitch(self.switch_arg_set_list.argList)

        if not self.model.IsfileExist(self.model_path + model_name):
            exists = False

        self.model.saveInTxt(self.model_path + model_name)

        return exists

    def switch_model_apply_cliced(self, name, create_switch_ui, nodes):
        """
        读取指定模式，并且应用
        :param name:
        :param create_switch_ui: 创建ui的函数指针
        :param nodes: 结点列表
        :return: ui控件组
        """
        arglist = self.model.readFromTxt(self.model_path + name)["switch"]
        print("read model: %s")
        print("read model list:")
        print(arglist)

        self.switch_arg_set_list = ArgvSet()

        widget_list = []
        for i in range(len(arglist)):
            # 创建控件
            widgets = create_switch_ui(i, nodes)

            # 设置参数
            self.switch_arg_set_list.setItem(arglist[i][0], arglist[i][1], i)
            print("apply add item: %s  %s" % (arglist[i][0], arglist[i][1]))

            # 设置结点的选择项
            index = widgets[0].findText(arglist[i][0])
            if index >= 0:
                widgets[0].setCurrentIndex(index)

            widget_list.append(widgets)

        self.switch_widget_list.clear()
        self.switch_widget_list = widget_list

        return widget_list

    def switch_model_del_clicked(self, name):
        """
        删除指定模式名的模式保存
        :param name:
        :return:
        """
        self.model.removeModelTxt(self.model_path + name)

    def switch_model_list_itemClicked(self, name):
        """
        获取指定模式名的描述
        :param name:
        :return:
        """
        return self.model.readFromTxt(self.model_path + name)["switch"]

    def compare_argset(self, list):
        """
        对比不一致的模式项
        :param list: 解析完成后的所有switch
        :return:
        """
        if len(self.switch_arg_set_list.argList) <= 0:
            return []
        return Model.diffList(self.switch_arg_set_list.argList, list)

    def compare_model_argset(self, list, mname):
        """
        对比模式保存中不一致项
        :param list:
        :param mname:
        :return:
        """
        return Model.diffList(self.model.readFromTxt(self.model_path + mname)["switch"], list)

    def remove_list(self, list):
        """
        删除已经有的参数项，和ui组
        :param list:
        :return:
        """
        entities = self.switch_arg_set_list.getEntities()
        index = []

        # 找到所有应该删除的项
        for i in range(len(entities)):
            if entities[i] in list:
                index.append(i)

        # 进行删除
        for i in reversed(index):
            # 删除参数
            self.switch_arg_set_list.delItem(i)
            # 删除控件
            widgets = self.switch_widget_list.pop(i)
            for w in widgets:
                w.deleteLater()
                del w
