#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11
# @Author  : RoyYoung

"""
解析避雷器信息的类
"""
from utils.Convert import Convert


class Lightning(object):
    def __init__(self, str):
        self.__parse(str)
        self.print()
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.vrefser = None
        self.vflash = None
        self.vzero = None
        self.col = None

    def __parse(self, str):
        self.c = str[0:2].strip()
        self.n1 = str[2:8].strip()
        self.n2 = str[8:14].strip()
        self.ref1 = str[14:20].strip()
        self.ref2 = str[20:26].strip()
        self.r = Convert.toDecimal(str[26:32].strip())
        self.a = Convert.toDecimal(str[32:38].strip())
        self.b = Convert.toDecimal(str[38:44].strip())
        self.length = Convert.toDecimal(str[44:50].strip())
        self.output = str[79:80].strip()

    def append(self, str):
        # 如果最后面不为空，则为参数值，否则是参数列表，参数列表还有只有一个值的特殊情况
        if str[78:80].strip():
            self.vrefser = Convert.toDecimal(str[8:25].strip())
            self.vflash = Convert.toDecimal(str[33:50].strip())
            self.vzero = Convert.toDecimal(str[58:75].strip())
            self.col = Convert.toDecimal(str[75:80].strip())
            print("lightning: vref:%.12g, vflash:%.12g, vzero:%.12g, col:%.12g" %
                  (self.vrefser, self.vflash, self.vzero, self.col))
        elif str[70:75].strip():
            self.list1.append(Convert.toDecimal(str[8:25].strip()))
            self.list2.append(Convert.toDecimal(str[33:50].strip()))
            self.list3.append(Convert.toDecimal(str[58:75].strip()))
            print("%.12g, %.12g, %.12g" % (self.list1[-1], self.list2[-1], self.list3[-1]))
        else:
            self.list1.append(Convert.toDecimal(str[8:25]))
            print("%g" % (self.list1[-1]))

    def generate(self):
        #      c    n1  n2  ref1 ref2 r   a    b   len
        str = "%-2s%-6s%-6s%-6s%-6s%+6s%+6s%+6s%+6s" % (self.c, self.n1, self.n2, self.ref1, self.ref2,
                                                        Convert.toStrPoint(self.r),
                                                        Convert.toStrPoint(self.a),
                                                        Convert.toStrPoint(self.b),
                                                        Convert.toStrPoint(self.length))
        # output
        if self.output:
            str += '%+30s' % self.output
        str += '\n'

        # 带参数
        if self.vrefser:
            #       空格     空格      空格
            str += "%8s%+17s%8s%+17s%8s%+17s%+5s\n" % \
                   ('', Convert.toStrPoint(self.vrefser),
                    '', Convert.toStrPoint(self.vflash),
                    '', Convert.toStrPoint(self.vzero), Convert.toStr(self.col))

            for i in range(len(self.list1) - 1):
                #       空格     空格      空格
                str += "%8s%+17s%8s%+17s%8s%+17s\n" % \
                       ('', Convert.toStrOrSN(self.list1[i]),
                        '', Convert.toStrOrSN(self.list2[i]),
                        '', Convert.toStrOrSN(self.list3[i]))

            #       空格
            str += "%8s%+17s\n" % ('', Convert.toStrOrSN(self.list1[-1]))

        return str

    def print(self):
        print("lightning: n1:%s, n2:%s, b:%.12g, output:%s" %
              (self.n1, self.n2, self.b, self.output))
