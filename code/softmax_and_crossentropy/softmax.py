# -*- coding: utf-8 -*-
"""
@Time    ： 2022/1/2 22:18
@Auth    ： liuhy
@File    ： softmax.py
@PROJECT ： lhy-nlp 
@Motto   ： ABC(Always Be Coding)

"""
import numpy as np
from icecream import ic

feature = np.random.randint(1, 10, 2)
print(feature)


def softmax(a, data=feature):
    #处理a的值 防止a特别大使得exp（a）变得特别大将内存撑爆
    print(np.max(feature))
    return np.exp(a-np.max(feature)) / np.sum(np.exp(e - np.max(feature)) for e in data)


def cross_entropy(y, y_hat):
    return -np.sum(y * np.log(y_hat))

s = 0
y_hat = []
for ans in (softmax(x, feature) for x in feature):
    y_hat.append(ans)
    s += ans
    ic('现在的总概率为{}'.format(s))


y = [1,0]
y_hat = [0.5,0.5]

ic(y_hat)
ic(cross_entropy(y,y_hat))