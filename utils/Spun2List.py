import random

import numpy as np


class Spun2List(object):
    def __init__(self, model, value, n):
        self.__model = model
        self.__value = value
        self.__times = n
        self.result = []

    def __split_value(self, value):
        if len(value) <= 2:
            return
        result = value.split('-')
        return result

    def getList(self):
        if self.__model == 's':  # 单值模式
            for i in range(0, self.__times):
                self.result.append(float(self.__value))

        if self.__model == 'p':  # 步长模式
            stepList = self.__split_value(self.__value)
            stepLen = (float(stepList[1]) - float(stepList[0])) / (self.__times - 1)
            for i in range(0, self.__times):
                self.result.append(i * stepLen + float(stepList[0]))

        if self.__model == 'u':  # 均匀模式
            uniformList = self.__split_value(self.__value)
            for i in range(0, self.__times):
                self.result.append(random.uniform(float(uniformList[0]), float(uniformList[1])))

        if self.__model == 'n':  # 正态分布
            normalList = self.__split_value(self.__value)
            up = float(normalList[1])
            down = float(normalList[0])
            loc = (down + up) / 2
            scale = (loc - down) / 4  # +-4个scale占有分布的99.99以上
            i = 0
            while i < self.__times:
                normalNum = np.random.normal(loc, scale)
                if up >= normalNum >= down:  # 不超过上下限
                    self.result.append(normalNum)
                    i += 1
                else:
                    continue
        return self.result


# for test
if __name__ == '__main__':
    test = Spun2List('n', '1-4', 5)
    list = test.getList()
    print(list)
