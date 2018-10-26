#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23
# @Author  : RoyYoung

"""
用于参数设置的底层实现类
"""


class ArgvSet(object):
    instance = None

    def __init__(self):
        # 对于每一种组件，使用一个二维数组存放，如: [['switch_1', "u_0_0.2"], ['switch_2', "s_0_3"]]
        # 二维数组存放了该组件的左右结点和一个模式变换的数组
        self.argList = []

    def add(self):
        """
        添加一个空的item
        :return:
        """
        self.argList.append(["", ""])

    # def addItem(self, entity, arg):
    #     """
    #     添加一项
    #     :param entity:
    #     :param arg:
    #     :return:
    #     """
    #     self.argList.append([entity, arg])

    def setItem(self, entity, arg, index):
        """
        添加一项
        :param entity:
        :param arg:
        :param index:
        :return:
        """
        self.argList[index][0] = entity
        self.argList[index][1] = arg

    def setEntity(self, entity, index):
        """
        获取实体的引用，如果索引超过当前长度，则为添加新的一行，否则是修改原有行
        :param entity:
        :param index:
        :return:
        """
        if index >= len(self.argList):
            self.argList.append([entity, ''])
        else:
            self.argList[index][0] = entity

    def setArg(self, str, index):
        """
        获取该实体对应的参数设置
        :param str:
        :param index:
        :return:
        """
        self.argList[index][1] = str

    def delItem(self, index):
        if index < len(self.argList):
            self.argList.pop(index)

    def getArg(self, index):
        return self.argList[index][1]

    def getEntity(self, index):
        return self.argList[index][0]

    def getItem(self, index):
        if index < len(self.argList):
            return self.argList[index]
        else:
            return None

    def getEntities(self):
        """
        获取swithc列表
        :return:
        """
        list = []
        for i in self.argList:
            list.append(i[0])
        return list


if __name__ == "__main__":
    pass
