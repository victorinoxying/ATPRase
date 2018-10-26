#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/21
# @Author  : RoyYoung

"""
output类，存放output列表
"""


class Output(object):
    def __init__(self, str):
        self.output = []
        for i in str.split():
            self.output.append(i.strip())
        self.print()

    def generate(self):
        str = "  "
        for i in range(len(self.output)):
            str += "%-6s" % self.output[i]

            # 每行输出13个
            if (i + 1) % 13 == 0 and (i + 1) != len(self.output):
                str += "\n  "
        str += "\n"
        return str

    def print(self):
        print(self.output)
