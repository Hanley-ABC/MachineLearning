# -*- coding: utf-8 -*-
"""
@Time    ： 2021/12/23 21:30
@Auth    ： liuhy
@File    ： cut_wood.py
@PROJECT ： lhy-nlp 
@Motto   ： ABC(Always Be Coding)

给定一个不同长度的木头的价格表 计算一个木头的最佳出售价格
"""
from collections import defaultdict
from functools import lru_cache

# 价格表
prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 33]

complete_price = defaultdict(int)

for i, p in enumerate(prices): complete_price[i + 1] = p
print(prices)
# ache_price = {0: 0}


@lru_cache(maxsize=2 ** 10)
def get_best_price(length):
    if length <= 0:return 0
    best_price = complete_price[length]
    for i in range(1, length // 2 + 1):
        price = get_best_price(i) + get_best_price(length - i)
        best_price = price if price > best_price else best_price

    # ache_price[length] = best_price
    return best_price


if __name__ == '__main__':
    for length in range(1, 1000):
        print('长度为{}的木头最佳的价格是:{}元'.format(length, get_best_price(length)))
