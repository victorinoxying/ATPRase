#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11
# @Author  : RoyYoung

"""
第一个信息类
"""

# TODO 不知道头部信息是否会使用，先直接记录
from utils.AtpSetting import AtpSetting
from utils.Convert import Convert


class Head(object):

    def __init__(self, s1, s2):
        """
        解析头部信息
        :param s1: 第一行信息
        :param s2: 第二行信息
        :return:
        """
        # self.__parse(s1, s2)
        self.s2 = s2
        self.step = 0.0
        self.tMax = 0.0

        self.__parse(s1)

    def __parse(self, s):
        """
        解析头部的步长和最大时间
        :param s:
        :return:
        """
        list = s.split()
        self.step = Convert.toDecimal(list[0])
        self.tMax = Convert.toDecimal(list[1])
        AtpSetting.set_time_max(self.tMax)

    """
    示例输出：
    C  dT  >< Tmax >< Xopt >< Copt >
       2.E-6     1.2                
         500       1       0       0       1       0       0       1       0
    C        1         2         3         4         5         6         7         8
    C 345678901234567890123456789012345678901234567890123456789012345678901234567890
    """

    def generate(self):
        str = 'C  dT  >< Tmax >< Xopt >< Copt ><Epsiln>\n' \
              + '%+8s%+8.2s%24s' % (Convert.toStrSN(self.step, 0), self.tMax, '') + '\n' \
              + self.s2 + '\n' \
              + 'C        1         2         3         4         5         6         7         8\n' \
              + 'C 345678901234567890123456789012345678901234567890123456789012345678901234567890\n'
        return str


def __parse(self, s1, s2):
    pass
