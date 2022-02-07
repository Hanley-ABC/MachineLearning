# -*- coding: utf-8 -*-
"""
@Time    ： 2021/12/23 21:35
@Auth    ： liuhy
@File    ： water_pour.py
@PROJECT ： lhy-nlp 
@Motto   ： ABC(Always Be Coding)

有两个杯子，A杯子容量90ml，B杯子容量40ml。假设现在需要得到 X ml 的水，请问能不能通过这两个杯子准确的量出来，
如果能怎么量。
"""

import time
# a:A杯子的初始水量；b：B杯子的初始水量；A：A杯子的容量；B：B杯子的容量
def successor(a, b, A, B):
    return {
        (0, b): '倒空A',
        (a, 0): '倒空B',
        (A, b): '装满A',
        (a, B): '装满B',
        (0, a + b) if (a + b) <= B else (a + b - B, B): '把A倒进B',
        (a + b, 0) if (a + b) <= A else (A, a + b - A): '把B倒进A'
    }


def search_solution(capacity1,capacity2,goal,start=(0,0)):

    # 定义set集合，储存计算过的状态
    explored = set()
    # 定义paths记录如何从初始状态走到当前状态的
    paths = [[('init',start)]]
    # 如果需要求所有可行的方案的话就把每一种方案都放在这里边
    lesspath = []

    # 如果目标值goal 在初始状态start中 返回初始状态即可
    if goal in start: return paths.pop(0)

    while paths:
        path = paths.pop(0)
        (x,y) = path[-1][-1]
        for stat,action in successor(x,y,capacity1,capacity2).items():
            if stat in explored:continue
            newpath = path+ [(action,stat)]

            if goal in stat:
                # return newpath
                time.sleep(2)
                lesspath.append(newpath)
                # 使用yield 可以直接返回结果同时不阻断程序的正常运行，适用于高延迟的场景
                # yield newpath
                return newpath
            paths.append(newpath)
            explored.add(stat)
    # return [('None')]
    # return lesspath


if __name__ == '__main__':

    answer =(search_solution(90,40,(n*10),(0,0)) for n in range (3))

    print(type(answer))
    j = 1
    for path in answer:
        i=0
        for i,s in enumerate(path):
            print('step {}:{}'.format(i,s))
        print('这是第{}种方式，它总共需要{}步'.format(j,i))
        j += 1