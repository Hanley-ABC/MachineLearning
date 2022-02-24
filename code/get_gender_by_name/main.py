# -*- coding: utf-8 -*-
"""
@Time    ： 2022/2/24 21:46
@Auth    ： liuhy
@File    ： main.py
@PROJECT ： MachineLearning 
@Motto   ： ABC(Always Be Coding)

"""
# from ngender import guess
#
#
# name = '王琳'
# result = guess(name)
#
# print('名字为{}的人,性别为：{} 的概率为：{}'.format(name, '男' if result[0] == 'male' else '女', result[1]))


import pandas as pd
import numpy as np

names_dataset = pd.read_csv('charfreq.csv')

female_total = np.sum(names_dataset['female'])
male_total = np.sum(names_dataset['male'])
total = female_total + male_total

names_dataset['char_male_freq'] = names_dataset.apply(lambda row: (1. * row['male'] / male_total), axis=1)
names_dataset['char_female_freq'] = names_dataset.apply(lambda row: (1. * row['female'] / female_total), axis=1)

char_freq = {}
for _, row in names_dataset.iterrows():
    char_freq[row['char']] = (row['char_male_freq'], row['char_female_freq'])
print('run=======')

def get_gender(name):
    pm = get_p(name=name, gender=0)
    pf = get_p(name=name, gender=1)
    if pf > pm:
        return 'female', pf / (pf + pm)
    else:
        return 'male', pm / (pf + pm)


def get_p(name, gender):
    p = 1
    for name_char in name:
        p *= char_freq[name_char][gender]

    p *= (male_total / total) if gender == 0 else (female_total / total)
    return p


if __name__ == '__main__':
    print(get_gender(name='洪宇'))
