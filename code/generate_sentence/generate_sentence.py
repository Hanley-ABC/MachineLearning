# -*- coding: utf-8 -*-
"""
@Time    ： 2021/12/22 00:55
@Auth    ： liuhy
@File    ： generate_sentence.py
@PROJECT ： lhy-nlp 
@Motto   ： ABC(Always Be Coding)

"""
import random

grammer = """
句子 = 主语 谓语 宾语
主语 = 你 ｜ 我 ｜ 她 ｜ 他
谓语 = 吃 ｜ 玩 ｜ 喝
宾语 = 水果 ｜ 皮球 ｜ 牛奶
"""

def get_grammer_by_description(grammer_str):
    grammer_gen = dict()

    for line in grammer_str.split("\n"):
        if not line.strip():continue
        stmt,expr = line.split("=")
        grammer_gen[stmt.strip()] = expr.strip().split("｜")

    # print("grammer_gen:{}".format(grammer_gen))
    return grammer_gen

def generate_sentence(grammer, target = '句子'):
    if target not in grammer : return target

    expr = random.choice(grammer.get(target))

    return ''.join([generate_sentence(grammer,e.strip()) for e in expr.split()])



if __name__ == "__main__":
    grammer = get_grammer_by_description(grammer)
    print("generate:")
    for i in range(10):
        print(generate_sentence(grammer))