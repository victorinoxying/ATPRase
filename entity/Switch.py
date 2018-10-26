#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11
# @Author  : RoyYoung

"""
switch解析
"""
from utils.Convert import Convert


class Switch(object):
    def __init__(self, str):
        self.__parse(str)
        self.print()

    def __parse(self, str):
        self.c = str[0:2].strip()
        self.n1 = str[2:8].strip()
        self.n2 = str[8:14].strip()
        self.tclose = Convert.toDecimal(str[14:24].strip())
        self.top = Convert.toDecimal(str[24:34].strip())
        self.ie = Convert.toDecimal(str[34:44].strip())
        self.vf = Convert.toDecimal(str[44:54].strip())
        self.type = str[54:64].strip()
        self.output = str[79:80].strip()

    def getNodes(self):
        """
        返回左右结点组成的字符串
        :return:
        """
        return self.n1 + '-' + self.n2

    def generate(self):
        #      c    n1  n2   TcloseTop  Ie   vf    type  空格 output
        str = "%-2s%-6s%-6s%+10s%+10s%+10s%+10s%+10s%15s%+1s\n" % \
              (self.c, self.n1, self.n2, Convert.toStrPoint(self.tclose, 5), Convert.toStrPoint(self.top, 5),
               Convert.toStrPoint(self.ie, 5), Convert.toStrPoint(self.vf, 5), self.type, '', self.output)
        return str

    def clone(self):
        """
        复制当前组件
        :return:
        """
        return Switch(self.generate().strip('\n'))

    def print(self):
        print("switch: c:%s, n1:%s, n2:%s, tclose:%f, top:%f, ie:%s, vf:%s, type:%s, output:%s" %
              (self.c, self.n1, self.n2, self.tclose, self.top, self.ie, self.vf, self.type, self.output))
