#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/20
# @Author  : RoyYoung

"""
生成atp类
"""
import os
import shutil

from atp.ParseHandler import ParseHandler
from utils.ArgvToList import ArgvToList
from utils.AtpBat import AtpBat
from utils.AtpSetting import AtpSetting
from utils.Convert import Convert


class CreateAtp(object):
    def __init__(self, path, fileName, parseHandler):
        self.__path = path
        self.__fileName = fileName
        self.__handler = parseHandler

        self.__switch_list = []

    def create(self, total, argDic):
        """
        生成atp文件的方法
        :param total: 总次数
        :param argDic: 所有参数设置的字典 {“switch”：swtich_arg_set}
        :return:
        """
        for time in range(total):
            # 初始化本地的组件列表
            branch = self.__handler.branch
            lightning = self.__handler.lightning
            lcc = []
            switch = []
            source = []
            output = []

            # 开关参数设置
            entities = argDic["switch"].getEntities()

            for k, v in self.__handler.switch.items():
                # 没有设置参数
                if k not in entities:
                    switch.append(v.clone())
                    continue

                # 针对一个元件多个结点参数设置情况
                # 如果该结点在参数设置中存在
                while k in entities:
                    # 获取结点index，删除该结点，获取arglist
                    index = entities.index(k)
                    argList = ArgvToList.toList(argDic['switch'].getArg(index), total, time)
                    entities.pop(index)

                    # 获取参数设置后的结点
                    argSwitch = []
                    for i in range(len(argList)):
                        # 第奇数个参数，闭合
                        if i % 2 == 0:
                            temp = v.clone()
                            temp.tclose = Convert.offsetRandom(Convert.toDecimal(argList[i]))
                            argSwitch.append(temp)
                        # 第偶数个参数，断开
                        elif i % 2 == 1:
                            argSwitch[i // 2].top = Convert.offsetRandom(Convert.toDecimal(argList[i]))
                            # temp.top = Convert.toDecimal(argList[i])

                    # 参数个数多余两个，并且为奇数，即最后一个的top没有值
                    if (len(argList) > 2) and (len(argSwitch) // 2 == 1):
                        argSwitch[-1].top = AtpSetting.get_time_max()

                    switch.extend(argSwitch)

            # 新建目录和文件
            dir = self.__path + '/' + self.__fileName + "_%d" % time
            if not os.path.exists(dir):
                os.mkdir(dir)
            shutil.copy(AtpBat.getAtpPath(), dir)
            self.__file = open(dir + "/" + self.__fileName + '.atp', 'w+')

            # 写入文件开头部分
            self.__file.write('BEGIN NEW DATA CASE\n')
            self.__infoWrite(self.__handler.info)
            self.__headWrite(self.__handler.head)
            self.__branchWrite(self.__handler.branch.values())
            self.__lightningWrite(self.__handler.lightning)
            self.__lccWrite(self.__handler.lcc)
            self.__switchWrite(switch)
            self.__sourceWrite(self.__handler.source.values())
            self.__outputWrite(self.__handler.output)
            # 写入文件结尾
            self.__file.writelines(
                ["BLANK BRANCH\n",
                 "BLANK SWITCH\n",
                 "BLANK SOURCE\n",
                 "BLANK OUTPUT\n",
                 "BLANK PLOT\n",
                 "BEGIN NEW DATA CASE\n",
                 "BLANK\n"])
            self.__file.close()

    def __argSet(self):
        """
        先根据设定的参数，来配置新的实例项
        :return:
        """
        pass

    def __infoWrite(self, info):
        """
        写入开头注释部分
        :param info:
        :return:
        """
        self.__file.write(info.generate())

    def __headWrite(self, head):
        """
        写入第一个信息
        :param head:
        :return:
        """
        self.__file.write(head.generate())

    def __branchWrite(self, list):
        """
        写入branch信息
        :param list:
        :return:
        """
        self.__file.writelines(['/BRANCH\n',
                                'C < n1 >< n2 ><ref1><ref2>< R  >< L  >< C  >\n',
                                'C < n1 >< n2 ><ref1><ref2>< R  >< A  >< B  ><Leng><><>0\n'])
        for i in list:
            self.__file.write(i.generate())

    def __lightningWrite(self, list):
        """
        雷电信息
        :param list:
        :return:
        """
        for i in list:
            self.__file.write(i.generate())

    def __lccWrite(self, list):
        """
        lcc信息
        :param list:
        :return:
        """
        for i in list:
            self.__file.write(i.generate())

    def __switchWrite(self, list):
        """
        switch信息
        :param list:
        :return:
        """
        self.__file.writelines(["/SWITCH\n", "C < n 1>< n 2>< Tclose ><Top/Tde ><   Ie   ><Vf/CLOP ><  type  >\n"])
        for i in list:
            self.__file.write(i.generate())

    def __sourceWrite(self, list):
        """
        source信息
        :param list:
        :return:
        """
        self.__file.writelines(
            ["/SOURCE\n", "C < n 1><>< Ampl.  >< Freq.  ><Phase/T0><   A1   ><   T1   >< TSTART >< TSTOP  >\n"])
        for i in list:
            self.__file.write(i.generate())

    def __outputWrite(self, output):
        """
        output信息
        :param list:
        :return:
        """
        self.__file.write("/OUTPUT\n")
        self.__file.write(output.generate())


if __name__ == "__main__":
    parseHandler = ParseHandler()
    parseHandler.parse(r"C:\Users\Administrator\Desktop\atp\方式1-N-1-主变合环-涂天线-单相重合闸-0.7s.atp")
    create = CreateAtp(r"C:\Users\Administrator\Desktop\atp\abc", parseHandler)
    create.create()
