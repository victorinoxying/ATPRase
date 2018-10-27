#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11
# @Author  : RoyYoung

"""
转换数值和字符串的类
"""
import random
from decimal import Decimal
from utils.AtpSetting import AtpSetting


class Convert(object):
    @staticmethod
    def toDecimal(str):
        """
        静态方法
        将字符串转换为Decimal
        :return:
        """
        return Decimal(str if str != "" else "0")

    @staticmethod
    def toStrPoint(decimal, precision=12):
        """
        将decimal转为字符串,带小数点
        结果可能为空
        :return:
        """
        format = "%." + str(precision) + "s"
        return '' if decimal == 0 else format % str(decimal.quantize(Decimal('0.00000000000000'))).strip('0')

    @staticmethod
    def toStr(decimal, precision=12):
        """
         将decimal转为字符串,不做任何处理
        结果可能为空
        :return:
        """
        format = '%.' + str(precision) + 's'
        return '' if decimal == 0 else format % str(decimal).strip('0')

    @staticmethod
    def toStrSN(decimal, precision=10):
        """
        将decimal转为科学计数法字符串
        结果一定不为空，因为decimal不为0
        :return:
        """
        format = '%.' + str(precision) + 'E'
        return format % decimal

    @staticmethod
    def toStrOrSN(decimal, precision=10):
        """
        仅适用于lightning
        根据当前数字，动态选择是标准格式还是科学计数法
        :return:
        """
        # 数字太小的转为科学计数法
        if (decimal < 0.01):
            return '%.10E' % decimal

        return '%.16s' % str(decimal)

    @staticmethod
    def offsetRandom(value):
        """
        偏移量随机
        :return:
        """
        v = random.random() * AtpSetting.get_time_offset() * 2 - AtpSetting.get_time_offset()
        return value + Decimal(v)


if __name__ == '__main__':
    # print(Convert.toStrOrSN(Decimal('5040.0005616581896800')))
    # print(Convert.toStrPoint('1'))
    # print(Convert.toStrSN(5040.0005616581896800, 3))
    tclose = Convert.offsetRandom(Convert.toDecimal('1'))
    print(tclose)
