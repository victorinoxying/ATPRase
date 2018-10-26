#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11
# @Author  : RoyYoung

"""
解析LCC
"""


# TODO LCC的lib文件还有问题，暂时不解析

class Lcc(object):
    def __init__(self, str):
        self.__nodes = []

        infos = str.split(',')
        self.path = infos[1].strip()

        for i in infos[2:]:
            # 这里的结点会有#号，如TZC###，请通过getNodes方法获取所有结点
            self.__nodes.append(i.strip())

        self.print()

    def getNodes(self):
        """
        获取所有结点
        :return:
        """
        list = []
        for i in self.__nodes:
            list.append(i.strip("#"))
        return list

    def generate(self):
        # 路径
        str = "$INCLUDE, %s $$\n  " % (self.path)
        for i in range(len(self.__nodes)):
            str += ", %6s" % (self.__nodes[i])
            # 每行输出9个
            if (i + 1) % 9 == 0 and (i + 1) != len(self.__nodes):
                str += " $$\n  "
        str = str.rstrip()
        str += '\n'
        return str

    def print(self):
        print("lcc: path:%s, nodes:%s" % (self.path, self.__nodes))
