# -*- coding: utf-8 -*-
"""
@Time    ： 2022/1/2 23:02
@Auth    ： liuhy
@File    ： cross_entropy.py
@PROJECT ： lhy-nlp 
@Motto   ： ABC(Always Be Coding)

"""
import numpy as np


def cross_entropy(y, y_hat):
    return -np.sum(y * np.log(y_hat))
