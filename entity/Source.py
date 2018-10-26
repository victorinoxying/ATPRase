#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11
# @Author  : RoyYoung

"""
解析source
"""
from utils.Convert import Convert


class Source(object):
    def __init__(self, str):
        self.__parse(str)
        self.print()

    def __parse(self, str):
        self.c = str[0:2].strip()
        self.n1 = str[2:8].strip()
        self.num = str[8:10].strip()
        self.ampl = Convert.toDecimal(str[10:20].strip())
        self.freq = Convert.toDecimal(str[20:30].strip())
        self.phase = Convert.toDecimal(str[30:40].strip())
        self.a1 = Convert.toDecimal(str[40:50].strip())
        self.t1 = Convert.toDecimal(str[50:60].strip())
        self.tstart = Convert.toDecimal(str[60:70].strip())
        self.tstop = Convert.toDecimal(str[70:80].strip())

    def getNodes(self):
        """
        返回左右结点组成的字符串
        :return:
        """
        return self.n1

    def generate(self):
        #      c   n1   <>   ampl freq  phase a1   t1    TstartTstop
        str = "%-2s%-6s%+2s%+10s%+10s%+10s%+10s%+10s%+10s%+10s\n" % \
              (self.c, self.n1, self.num, Convert.toStrPoint(self.ampl), Convert.toStrPoint(self.freq),
               Convert.toStrPoint(self.phase),
               Convert.toStrPoint(self.a1), Convert.toStrPoint(self.t1), Convert.toStrPoint(self.tstart),
               Convert.toStrPoint(self.tstop))
        return str

    def print(self):
        print("source: c:%s, n1:%s, num:%s, ampl:%f, freq:%f, phase:%f, a1:%f, t1:%f, tstart:%f, tstop:%f" %
              (self.c, self.n1, self.num, self.ampl, self.freq, self.phase, self.a1, self.t1, self.tstart, self.tstop))
