#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/24
# @Author  : RoyYoung

"""
设置全局配置参数的类
"""


class AtpSetting(object):
    # 时间偏移量
    __time_offset = 0.0001
    # 最大时间
    __time_max = 0

    @classmethod
    def get_time_offset(cls):
        return cls.__time_offset

    @classmethod
    def set_time_offset(cls, offset):
        cls.__time_offset = offset

    @classmethod
    def get_time_max(cls):
        return cls.__time_max

    @classmethod
    def set_time_max(cls, time):
        cls.__time_max = time


if __name__ == '__main__':
    AtpSetting.set_time_offset(1)
    print(AtpSetting.get_time_offset())
