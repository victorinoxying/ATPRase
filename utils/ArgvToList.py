#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/25
# @Author  : RoyYoung

"""
根据参数设置转换为值的工具类
"""
import random

import numpy as np


class ArgvToList(object):
    @staticmethod
    def toList(str, total, time):
        """
        获取指定第几次的值
        :param total: 总共取值的次数
        :param time: 需要取第几次的值
        :return:
        """
        result = []
        argv = str.split(';')

        for i in argv:
            li = i.split('_')
            # 单值
            if li[0] == 's':
                result.append(li[1])
            # 步长
            elif li[0] == 'p':
                step = (float(li[2]) - float(li[1])) / (total - 1)
                result.append(float(li[1]) + step * (time - 1))
            # 均匀分布
            elif li[0] == 'u':
                result.append(random.uniform(float(li[1]), float(li[2])))
            # 正态分布
            elif li[0] == 'n':
                down = float(li[1])
                up = float(li[2])
                loc = (down + up) / 2
                scale = (loc - down) / 4  # +-4个scale占有分布的99.99以上
                while True:
                    normalNum = np.random.normal(loc, scale)
                    if up >= normalNum >= down:  # 不超过上下限
                        result.append(normalNum)
                        break

        return result


if __name__ == '__main__':
    a = ArgvToList.toList('s_1;s_2;s_3;', 1, 1)
    # a = ArgvToList.toList('u_1_2;n_4_5;p_8_9;', 3, 1)
    print(a)
