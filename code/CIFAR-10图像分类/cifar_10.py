# -*- coding: utf-8 -*-
"""
@Time    ： 2022/1/18 23:04
@Auth    ： liuhy
@File    ： cifar_10.py
@PROJECT ： lhy-nlp 
@Motto   ： ABC(Always Be Coding)

"""
import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms

import model as M
import train as T

##定义对图像的各种变换操作，包括把array转换为tensor，对图像做正则化
# transforms.Compose主要是用于常见的一些图形变换，例如裁剪、旋转
# 遍历list数组，对img依次执行每个transforms操作
transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.4914, 0.48216, 0.44653),
                                                     (0.24703, 0.24349, 0.26159))])
# 导出torchvision里的CIFAR10数据集，root是把数据下载之后存放的目录，
# train控制是不是在训练阶段，download控制是不是需要下载，transform把一系列的图像变换传入进来。
trainset = torchvision.datasets.CIFAR10(root='/Users/liuhy/workspace/NLP/learning_materials/nlp基础/第七章/',
                                        train=True,
                                        download=False,
                                        transform=transform)
testset = torchvision.datasets.CIFAR10(root='/Users/liuhy/workspace/NLP/learning_materials/nlp基础/第七章/',
                                       train=False,
                                       download=False,
                                       transform=transform)
# 用来把训练数据分成多个小组，此函数每次抛出一组数据。
trainloader = torch.utils.data.DataLoader(trainset,
                                          batch_size=16,
                                          shuffle=True)
# 用来把测试数据分成多个小组，此函数每次抛出一组数据。
testloader = torch.utils.data.DataLoader(testset,
                                         batch_size=16,
                                         shuffle=False)


# 把图片进行可视化展示
# 定义画图的函数
def imshow(inp, title=None):
    """Imshow for Tensor."""
    # 定义画图的画布
    fig = plt.figure(figsize=(30, 30))
    # 转换图片的纬度
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    # 对图片进行标准化
    inp = std * inp + mean
    # 整个图片数组的值限制在指定值a_min,与a_max之间
    inp = np.clip(inp, 0, 1)
    # 对图片进行可视化展示
    plt.imshow(inp, )
    plt.show()


if __name__ == '__main__':
    # 获取一个batch的数据
    inputs, classes = next(iter(trainloader))

    # 以网格的格式展示，作用是将若干幅图像拼成一幅图像
    out = torchvision.utils.make_grid(inputs)
    # plt.imshow()就可显示图片同时也显示其格式。
    imshow(out, title=[trainset.classes[x] for x in classes])

    net = M.Net()

    T.train(net=net, trainloader=trainloader, num_epochs=20)
