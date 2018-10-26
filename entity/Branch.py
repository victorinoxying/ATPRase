#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 10:37
# @Author  : RoyYoung

"""
解析branch中电容电阻电感
"""

from utils.Convert import Convert


class Branch(object):
    def __init__(self, str):
        self.__parse(str)
        self.print()

    def __parse(self, str):
        self.category = str[0:2].strip()
        self.n1 = str[2:8].strip()
        self.n2 = str[8:14].strip()
        self.ref1 = str[14:20].strip()
        self.ref2 = str[20:26].strip()
        self.r = Convert.toDecimal(str[26:32].strip())
        self.l = Convert.toDecimal(str[32:38].strip())
        self.c = Convert.toDecimal(str[38:44].strip())
        self.output = str[79:80].strip()

    def getNodes(self):
        """
        返回左右结点组成的字符串
        :return:
        """
        return self.n1 + '-' + self.n2

    def generate(self):
        """
        生成格式化的信息
        :return:
        """
        #      c    n1  n2  ref1 ref2 r   l    c
        str = "%-2s%-6s%-6s%-6s%-6s%+6s%+6s%+6s" % (self.category, self.n1, self.n2, self.ref1, self.ref2,
                                                    Convert.toStrPoint(self.r), Convert.toStrPoint(self.l),
                                                    Convert.toStrPoint(self.c))
        # output
        if self.output:
            str += '%+36s' % self.output

        str = str.rstrip()
        str += '\n'
        return str

    def print(self):
        print("branch: category:%s, n1:%s, n2:%s, ref1:%s, ref2:%s, r:%.14f, l:%.14f, c:%.14f, output:%s" %
              (self.category, self.n1, self.n2, self.ref1, self.ref2, self.r, self.l, self.c, self.output))
