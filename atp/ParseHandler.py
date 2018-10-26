#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 10:37
# @Author  : RoyYoung

"""
控制解析的类
"""
import collections

from entity.Branch import Branch
from entity.Head import Head
from entity.Info import Info
from entity.Lcc import Lcc
from entity.Lightning import Lightning
from entity.Output import Output
from entity.Source import Source
from entity.Switch import Switch


class ParseHandler(object):
    def __init__(self):
        """
        初始化的工作
        """
        self.info = None
        self.head = None
        self.lightning = []
        self.lcc = []
        # 使用字典方便查询
        self.branch = {}
        self.switch = collections.OrderedDict()
        self.source = {}
        self.output = None

    def parse(self, file):
        """
        解析总控制
        :param file: atp文件
        :return:
        """
        # 打开文件
        self.__atpFile = open(file, 'r')

        self.__line = self.__atpFile.readline().strip('\n')
        while not self.__line.startswith('BLANK'):
            # 开头的注释部分
            if self.__line == 'BEGIN NEW DATA CASE':
                self.__parseInfo()
                continue
            # 第一个信息
            if (self.__line.startswith('C  dT  >< Tmax >< Xopt >< Copt >')):
                self.__parseHead()
                continue

            # branch的信息
            if self.__line == '/BRANCH':
                self.__parseBranch()
                continue

            # switch的信息
            if self.__line == '/SWITCH':
                self.__parseSwitch()
                continue

            # source的信息
            if self.__line == '/SOURCE':
                self.__parseSource()
                continue

            # initial的信息
            if self.__line == '/INITIAL':
                self.__line = self.__atpFile.readline().strip('\n')
                continue

            # output的信息
            if self.__line == '/OUTPUT':
                self.__parseOutput()
                continue

            self.__line = self.__atpFile.readline().strip('\n')

        self.__atpFile.close()

    def __parseInfo(self):
        """
        解析文件开头的注释部分
        :return:
        """
        self.info = Info()
        self.__line = self.__atpFile.readline().strip('\n')

        while not self.__line.startswith('C  dT  >< Tmax >< Xopt >< Copt >'):
            self.info.append(self.__line)
            self.__line = self.__atpFile.readline().strip('\n')

    def __parseHead(self):
        """
        解析头部第一个信息
        :return:
        """
        s1 = self.__atpFile.readline().strip('\n')
        s2 = self.__atpFile.readline().strip('\n')
        self.head = Head(s1, s2)

        self.__line = self.__atpFile.readline().strip('\n')

    def __parseBranch(self):
        """
        解析branch信息
        :return:
        """
        # 跳过前两行
        self.__line = self.__atpFile.readline().strip('\n')
        self.__line = self.__atpFile.readline().strip('\n')
        self.__line = self.__atpFile.readline().strip('\n')

        while not self.__line.startswith('/', 0):
            # 如果以$INCLUDE 开头则是LCC线路
            if self.__line.startswith('$INCLUDE'):
                str = self.__line.strip('$$\n')
                # 如果以 $$ 结尾，则还有一行
                while self.__line.endswith('$$'):
                    self.__line = self.__atpFile.readline().strip('\n')
                    str += self.__line.strip('$$\n')

                self.__line = self.__atpFile.readline().strip('\n')
                self.lcc.append(Lcc(str))
                continue

            line = self.__line
            self.__line = self.__atpFile.readline().strip('\n')

            # 当前是一个组件，下一行是参数，则当前是一个雷电组件
            if (line[44:50].strip() == "" and self.__line[44:50].strip() != ""):
                self.lightning.append(Lightning(line))
                continue

            # 如果后面几个位置不为空，那么属于雷电的参数列表
            if line[44:50].strip() or len(line) == 25:
                self.lightning[-1].append(line)
                continue

            # 通过类别c来判断当前是属于已有的雷电还是一般的组件
            if self.lightning and line[0:2] == self.lightning[-1].c:
                self.lightning.append(Lightning(line))
            else:
                temp = Branch(line)
                self.branch[temp.getNodes()] = temp

    def __parseSwitch(self):
        """
        解析switch
        :return:
        """
        # 跳过第一行
        self.__line = self.__atpFile.readline().strip('\n')
        self.__line = self.__atpFile.readline().strip('\n')
        while not self.__line.startswith('/', 0):
            temp = Switch(self.__line)
            self.switch[temp.getNodes()] = temp
            self.__line = self.__atpFile.readline().strip('\n')

    def __parseSource(self):
        """
        解析source
        :return:
        """
        # 跳过第一行
        self.__line = self.__atpFile.readline().strip('\n')
        self.__line = self.__atpFile.readline().strip('\n')
        while not self.__line.startswith('/', 0):
            temp = Source(self.__line)
            self.source[temp.getNodes()] = temp
            self.__line = self.__atpFile.readline().strip('\n')

    def __parseOutput(self):
        """
        解析output
        :return:
        """
        self.__line = self.__atpFile.readline().strip('\n')
        out = ''
        while not self.__line.startswith('BLANK'):
            out += self.__line.strip('\n')
            self.__line = self.__atpFile.readline().strip('\n')

        self.output = Output(out)


if __name__ == '__main__':
    parseHandler = ParseHandler()
    parseHandler.parse(r"C:\Users\Administrator\Desktop\atp\方式1-N-1-主变合环-涂天线-单相重合闸-0.7s.atp")
    print(parseHandler.branch)
