import cgitb
import os
import struct

import matplotlib.pyplot as plt
import pandas

"""
pl4解析类
输入：pl4文件路径
输出：得到pl4二进制文件的解析结果——min，max，ave，dataFrame

b2any工具函数
getAllPoints得到所有节点
get_dataFrame得到默认数据（电流电压节点的所有时间点的数据矩阵）

save_txt(filename, ags_dict, model_num)
usage：
输入：   filename:项目路径
        ags_dict:用户定义的结果内容[绝对值bool，起始时间number，终止时间number，结果标签dict(例如所需要的某几个node)，结果类型dict(例如max，min，ave)]
        model_num:模式名
     example：
        dict = [False,0,0.003,['XX0005','VS'],['max','min','ave']]
        pl4.save_txt(r'D:\example', dict, 'model_example')
输出：将数据分别存到txt中

get_resultData(ags_dict)
输入如上例
输出： dict['min':xxx xxx , 'max':xxx xxx ...]，其中每一个value是一个series

drowPicture(filename, ags_dict, model_num, AllorPart)
usage:
输入： 前三个参数如上,最后一个AllorPart指的是选择总时间段内的数据图像，还是规定时间段内的图像
AllorPart可输入: 'all'(总时间段）,'select'（特定时间段）
"""


class pl4_Analysis(object):

    def __init__(self, ATPfile):
        self.__file = open(ATPfile + '.pl4', 'rb')
        BinarySteam = struct.iter_unpack('c', self.__file.read())  # 读取二进制数据
        self.__file.close()
        self.__binaryDict = []
        for i in BinarySteam:
            self.__binaryDict.append(i[0])

    # 二进制转换为其他数据类型的小工具
    def b2any(self, goal_type, sor, num):
        model = None
        for i in range(num):
            if i == 0:
                model = sor[i]
            else:
                model = model + sor[i]
        ans = struct.unpack(goal_type, model)[0]
        return ans

    # 根据二进制字典准备初始数据
    def __prepare(self):
        self.__time = self.b2any('19s', self.__binaryDict[:19], 19)  # 时间
        self.__pointNum = int(self.b2any('I', self.__binaryDict[19:23], 4))  # 存储节点总数
        self.__volNum = int(self.b2any('I', self.__binaryDict[23:27], 4) / 2)  # 显示电压数
        self.__totalDisplayNum = int(self.b2any('I', self.__binaryDict[27:31], 4) / 2)  # 总显示数
        self.__tacsNum = int(self.b2any('I', self.__binaryDict[31:35], 4))  # TACS节点数
        self.__dataBlockStart = self.b2any('I', self.__binaryDict[39:43], 4)  # 数据块其实位置
        self.__dataBlockEnd = self.b2any('I', self.__binaryDict[43:47], 4)  # 数据块结束位置
        self.__getNeededPoints()  # 得到所需要的节点
        self.__dataFrame = pandas.DataFrame()
        self.__selectedDF = pandas.DataFrame()

    # 得到所有的节点名称
    def getAllPoints(self):
        pointBinaryInfo = self.__binaryDict[47 + self.__tacsNum * 6:47 + self.__tacsNum * 6 + self.__pointNum * 6]
        self.__allPointName = []

        for i in range(0, len(pointBinaryInfo), 6):
            self.__allPointName.append(str(self.b2any('6s', pointBinaryInfo[i:i + 6], 6), encoding='gbk'))
        return self.__allPointName

    # 得到所需节点名称列表
    def __getNeededPoints(self):
        self.getAllPoints()

        vol_currentInfo = self.__binaryDict[47 + self.__tacsNum * 6 + self.__pointNum * 6:
                                            47 + self.__tacsNum * 6 + self.__pointNum * 6 + self.__totalDisplayNum * 8]
        # 电压电流点的索引
        point_index = []
        for i in range(0, len(vol_currentInfo), 8):
            point_index.append(self.b2any('I', vol_currentInfo[i:i + 4], 4))

        # 模型中的节点名称列表
        self.__pointInModel = []
        for i in range(0, self.__totalDisplayNum):
            self.__pointInModel.append(self.__allPointName[point_index[i] - 1])

    def __Analysis(self, start_time, end_time):
        self.__prepare()
        self.start_t = 0
        self.end_t = 0
        for i in range(0, self.__totalDisplayNum + 1):
            ans = []
            count = 0
            for j in range(self.__dataBlockStart - 1, self.__dataBlockEnd - 1, 4 * (self.__totalDisplayNum + 1)):

                ans.append(self.b2any('f', self.__binaryDict[j + i * 4:j + i * 4 + 4], 4))
                # 根据用户选择的起止时间，来标定数据中对应的时间区间起止点
                if i == 0:
                    if self.b2any('f', self.__binaryDict[j + i * 4:j + i + 4 * 4], 4) < start_time:
                        self.start_t = count
                    elif self.b2any('f', self.__binaryDict[j + i * 4:j + i + 4 * 4], 4) < end_time:
                        self.end_t = count + 1
                    count = count + 1
            if i == 0:
                self.__dataFrame.insert(i, 'time', ans)
            else:
                self.__dataFrame.insert(i, self.__pointInModel[i - 1].strip(), ans)

    def get_dataFrame(self):
        self.__Analysis(0, 99999)
        return self.__dataFrame

    def get_resultData(self, ags_dict):

        withTimeDic = ['time']
        self.__Analysis(ags_dict[1], ags_dict[2])
        if (ags_dict[3] != []) and (ags_dict[3] != ''):
            for x in range(len(ags_dict[3])):
                ags_dict[3][x] = ags_dict[3][x].strip()
                withTimeDic.append(ags_dict[3][x])

            # 存放用户需要的时间段及结果标签对应的数据
            self.__selectedDF = self.__dataFrame[ags_dict[3]][self.start_t:self.end_t]
            self.__drawDF = self.__dataFrame[withTimeDic][self.start_t:self.end_t]
        else:
            self.__selectedDF = self.__dataFrame.iloc[self.start_t:self.end_t, 1:]

        # 处理绝对值
        if ags_dict[0]:
            maxData = abs(self.__selectedDF.max())
            minData = abs(self.__selectedDF.min())
            aveData = self.__selectedDF.abs().mean()
        else:
            maxData = self.__selectedDF.max()
            minData = self.__selectedDF.min()
            aveData = self.__selectedDF.mean()

        # 不同的模式结果记录在不同的文件中
        result_dict = {}
        for tips in ags_dict[4]:
            if tips == 'max':
                result_dict[tips] = maxData
            if tips == 'min':
                result_dict[tips] = minData
            if tips == 'ave':
                result_dict[tips] = aveData
        return result_dict

    def save_txt(self, filename, ags_dict):
        resultDict = self.get_resultData(ags_dict)
        for key in resultDict:
            if key == 'max':
                filename_max = filename + '_max.txt'
                fileSteam_max = open(filename_max, 'a+')
                # 保证第一行是节点，后面的数据可追加
                if os.path.getsize(fileSteam_max.name) < 1:
                    for i in range(len(resultDict[key])):
                        fileSteam_max.write('%12s ' % resultDict[key].index[i])
                    fileSteam_max.write('\n')
                for i in range(len(resultDict[key])):
                    fileSteam_max.write('%10e ' % resultDict[key][i])
                fileSteam_max.write('\n')
                fileSteam_max.close()

            elif key == 'min':
                filename_min = filename + '_min.txt'
                fileSteam_min = open(filename_min, 'a+')
                # 保证第一行是节点，后面的数据可追加
                if os.path.getsize(fileSteam_min.name) < 1:
                    for i in range(len(resultDict[key])):
                        fileSteam_min.write('%12s ' % resultDict[key].index[i])
                    fileSteam_min.write('\n')
                for i in range(len(resultDict[key])):
                    fileSteam_min.write('%10e ' % resultDict[key][i])
                fileSteam_min.write('\n')
                fileSteam_min.close()

            elif key == 'ave':
                filename_ave = filename + '_ave.txt'
                fileSteam_ave = open(filename_ave, 'a+')
                # 保证第一行是节点，后面的数据可追加
                if os.path.getsize(fileSteam_ave.name) < 1:
                    for i in range(len(resultDict[key])):
                        fileSteam_ave.write('%12s ' % resultDict[key].index[i])
                    fileSteam_ave.write('\n')
                for i in range(len(resultDict[key])):
                    fileSteam_ave.write('%10e ' % resultDict[key][i])
                fileSteam_ave.write('\n')
                fileSteam_ave.close()
            else:
                return 'wrong'

    def drawPicture(self, filename, ags_dict, AllorPart):
        self.get_resultData(ags_dict)
        data = pandas.DataFrame()
        if AllorPart == 'all':
            data = self.__dataFrame
        elif AllorPart == 'select':
            data = self.__drawDF
        else:
            return 'wrong'
        x = data['time']
        y = data.iloc[:, 1:2]
        plt.plot(x, y)
        filename = filename + '_pl4.png'
        plt.savefig(filename)


if __name__ == '__main__':
    cgitb.enable(format='text')

    # pl4 = pl4_Analysis(r'D:\dataatp\myfirst')
    # dic = [True, 0, 0.003, ['XX0005', 'VS'], ['max', 'min', 'ave']]
    # pl4.save_txt(r'D:\dataatp\test', dic, 'model')
    # print(d);

    pl4 = pl4_Analysis(r'C:\Users\Administrator\Desktop\atp\方式1-N-1-主变合环-涂天线-单相重合闸-0.7s_0\方式1-n-1-主变合环-涂天线-单相重合闸-0.7s')
    dic = [False, 0.1, 0.2, ['DTA', 'DTB'], ['max', 'min']]
    b = pl4.drawPicture(r'C:\Users\Administrator\Desktop\atp\方式1-N-1-主变合环-涂天线-单相重合闸-0.7s_0\方式1-n-1-主变合环-涂天线-单相重合闸-0.7s',
                        dic, 'model', 'all')
    # d = a.get_resultData(c)
    # pl4.save_txt(r'D:\dataatp\test', dic, 'model')
    # print(d);

    # import matplotlib.pyplot as plt
    # b = a.get_dataFrame()
    # x = b['time']
    # y = b.iloc[:,1:2]
    # plt.plot(x,y)
    # plt.show()
