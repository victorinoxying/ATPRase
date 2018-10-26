#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/18
# @Author  : RoyYoung

"""
用于runAtp文件，来生成pl4文件
通过进程池，异步执行任务
这里的方法大部分都是类方法
"""
import cgitb
import concurrent
import os
import subprocess
import time
from concurrent import futures

from PyQt5.QtCore import QThread, pyqtSignal

from atp.CreateDoc import CreateDoc
from atp.pl4_Analysis import pl4_Analysis
from utils.AtpBat import AtpBat


class RunATP(QThread):
    # 更新进度条用的信号槽
    progressUpdated = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        # self.moveToThread(self)

        # runATP.exe的路径
        self.__runATPPath = AtpBat.getBatPath()
        # RunATP.__runATPPath = 'D:/ATPDraw/runATP_G.bat'

        # 进度条进度
        self.progress = 0

        # atp文件路径
        self.path = []
        # atp文件名
        self.fname = []
        # 分析pl4的dic
        self.dic = []

    def submit(self, path, fname, resultDic):
        """
        提交任务
        :param path: atp文件路径
        :param fileName: 文件名
        :param resultDic: 分析pl4用的dic
        :return:
        """
        self.path.append(path)
        self.fname.append(fname)
        self.dic.append(resultDic)

    def run(self):
        print('run')
        AtpBat.setAtpConf('1')
        time.sleep(0.1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = []
            for i in range(len(self.path)):
                futures.append(executor.submit(self.runJob, self.path[i], self.fname[i], self.dic[i]))
                # futures[executor.submit(self.runJob, self.path[i], self.fname[i], self.dic)] = i

            for future in concurrent.futures.as_completed(futures):
                try:
                    data = future.result()
                    print('run result: ' + data)
                except Exception as exc:
                    print('Generated an exception: %s' % exc)
                else:
                    if data:
                        self.progress += 1
                        print("progress: %d" % self.progress)
                        self.progressUpdated.emit(int(self.progress / len(self.path) * 100))

        self.progressUpdated.emit(100)
        self.clear()

    def runJob(self, path, fname, resultDic):
        """
        为了能被pickle，使用该函数
        用于runatp和分析pl4
        :param path:
        :param fname:
        :param [0, 0.003, ['XSA', 'XSB'], ['max', 'min', 'ave']]
            resultDic: ['start' : '', 'end' : '', 'output': [], 'value': ['max', 'min', 'ave']]
        :return:
        """
        print('runJob')
        # 提交任务
        # queue.put(1)
        print('submit')
        self.runATP(path, fname)
        self.analysePl4(path, fname, resultDic)
        # queue.get()
        print('complete')
        return 'complete'

    def runATP(self, path, fname):
        """
        调用runATP.exe进行分析
        :param fname:
        :return:
        """
        # cmd = RunATP.__runATPPath + " " + path + '/' + fileName
        # p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)

        cmd = path[0:2] + ' && cd ' + path + " && " + self.__runATPPath + ' ' + fname + '.atp'
        print("run atp path: %s, atp path: %s" % (self.__runATPPath, path + '/' + fname))
        print('run atp cmd: ' + cmd)

        FNULL = open(os.devnull, 'w')
        subprocess.call(cmd, shell=True, stdout=FNULL)

        print("run atp end")

    def analysePl4(self, path, fname, resultDic):
        # 如果没有生成pl4
        file = path + '/' + fname + '.pl4'
        if not os.path.isfile(file):
            print('pl4: %s not find, there is something error!' % (file))
            return

        if os.path.getsize(file) == 0:
            print("pl4 file: %s size is 0, run atp error!" % (file))
            return

        print('start analysePl4: %s' % (file))

        pl4 = pl4_Analysis(path + '/' + fname)

        # dic = [False, 0, 0.003, ['XX0005', 'VS'], ['max', 'min', 'ave']]
        dic = [False, float(resultDic['start']), float(resultDic['end']), resultDic['output'], resultDic['value']]

        print('pl4 result txt')
        pl4.save_txt(path + "/" + 'result', dic)

        print('pl4 result picture')
        # b = pl4.drawPicture(r'D:\dataatp\myfirst', dic, 'model', 'all')
        pl4.drawPicture(path + '/' + 'result', dic, 'all')

        print('pl4 doc')
        doc = CreateDoc()
        doc.addFilePara(fname)
        doc.addPicture(path + '/' + 'result')
        for i in resultDic['value']:
            doc.addTablePara(path + '/' + 'result', i)
        doc.saveDoc(path + '/' + 'result')

        print('analysePl4 end')

    def clear(self):
        """
        清空变量
        :return:
        """
        # 进度条进度
        self.progress = 0
        # atp文件路径
        self.path = []
        # atp文件名
        self.fname = []
        # 分析pl4的dic
        self.dic = []


if __name__ == '__main__':
    cgitb.enable(format='text')

    # dic = False, 0, 0.3, ['DTA', 'DTB'], ['max', 'min', 'ave']]
    dic = {'start': '0', 'end': '0.003', 'output': ['DTA', 'DTB'], 'value': ['max', 'min', 'ave']}

    runAtp = RunATP()
    runAtp.submit(r'C:\Users\Administrator\Desktop\atp\方式1-N-1-主变合环-涂天线-单相重合闸-0.7s_0', r'方式1-N-1-主变合环-涂天线-单相重合闸-0.7s',
                  dic)
    runAtp.start()
    runAtp.wait()
    # runAtp.runJob(r'C:\Users\Administrator\Desktop\atp\方式1-N-1-主变合环-涂天线-单相重合闸-0.7s_0', r'方式1-N-1-主变合环-涂天线-单相重合闸-0.7s', dic)
