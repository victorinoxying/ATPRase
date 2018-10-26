#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27
# @Author  : RoyYoung

"""
用于更新和同步atpdraw中的atp文件
控制f2以后的脚本操作
"""
import os


class AtpBat(object):
    @staticmethod
    def modify_bat(filePath):
        """
        修改bat脚本
        :param filePath:
        :return:
        """
        # 如果修改过，则以备份的脚本为准
        if os.path.exists(filePath + '.bak.bat'):
            os.remove(filePath)
        else:
            os.rename(filePath, filePath + '.bak.bat')

        bat = open(filePath + '.bak.bat')
        source = bat.readlines()
        bat.close()

        # 新建配置文件
        if not os.path.exists('conf'):
            os.mkdir('conf')
            atpConf = open('conf/atp.cfg', "w+")
            pathConf = open('conf/path.cfg', 'w+')
            batPath = open('conf/batPath.cfg', 'w+')
            atpConf.close()
            pathConf.close()
            batPath.close()

        # 写入bat路径
        batPath = open('conf/batPath.cfg', 'w+')
        batPath.write(filePath)

        # 获取配置文件路径
        acpath = os.path.abspath('conf\\atp.cfg')
        pcpath = os.path.abspath('conf\\path.cfg')
        print('atpConf config path: ' + acpath)
        print('pathConf config path: ' + pcpath)

        # 写入文件内容
        atpConf = open(filePath, "w+")
        # 为0直接退出
        atpConf.write('@echo off\nset /p var=<' + acpath + '\necho %1>' + pcpath + '\nif "%var%" == "0" (Exit)\n')
        for line in source:
            atpConf.write(line)
        atpConf.close()

    @staticmethod
    def setAtpConf(config):
        """
        修改配置文件内容
        :param config:
        :return:
        """
        f = open('conf/atp.cfg', 'w+')
        f.write(config)
        f.close()

    @staticmethod
    def getAtpPath():
        """
        获取bat脚本中atp文件路劲
        :return:
        """
        f = open('conf/path.cfg', 'r')
        path = f.readline().strip()
        f.close()
        print('read path.cfg: ' + path)
        return path

    @staticmethod
    def isBatExists():
        """
        判断是否配置工具路径
        :return:
        """
        if not os.path.exists('conf'):
            return False
        if not os.path.isfile('conf/batPath.cfg'):
            return False
        return True

    @staticmethod
    def getBatPath():
        """
        获取bat脚本路径
        :return:
        """
        file = open("conf/batPath.cfg")
        path = file.readline()
        file.close()
        return path
