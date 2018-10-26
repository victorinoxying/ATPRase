#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/22
# @Author  : RoyYoung

"""
关于ui的工具类
"""


class UIUtils(object):
    def deleteLayout(layout):
        if layout is not None:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
