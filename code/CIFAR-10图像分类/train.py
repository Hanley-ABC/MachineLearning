# -*- coding: utf-8 -*-
"""
@Time    ： 2022/1/19 21:29
@Auth    ： liuhy
@File    ： train.py
@PROJECT ： lhy-nlp 
@Motto   ： ABC(Always Be Coding)

"""

import time as time

import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm


def train(net, trainloader, num_epochs, lr=3e-4):
    # 定义损失函数-交叉熵
    criterion = nn.CrossEntropyLoss()
    # 定义优化器，将神经网络的参数都传入优化器，并定义学习率
    optimizer = optim.Adam(net.parameters(), lr)

    losses = []
    since = time.time()
    net.train()
    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch + 1, num_epochs))

        running_loss = 0.0
        running_corrects = 0
        # 从trainloader里循环取出每一批次数据，
        for data in tqdm(trainloader):
            inputs, labels = data
            inputs = inputs.view(-1, 32 * 32 * 3)
            # optimizer.zero_grad()
            outputs = net(inputs)
            optimizer.zero_grad()
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            _, preds = torch.max(outputs, 1)

            # 一个批次数据的损失函数的计算
            running_loss += loss.item() * inputs.size(0)
            # 一个批次数据准确率的计算
            running_corrects += torch.sum(preds == labels.data)

        epoch_loss = running_loss / trainloader.dataset.data.shape[0]
        epoch_acc = running_corrects.double() / trainloader.dataset.data.shape[0]
        losses.append(epoch_loss)
        print('train Loss: {:.4f} Acc: {:.4f}'.format(
            epoch_loss, epoch_acc))
        print('-' * 10)

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_title('-loss-')
    x = [i for i in range(num_epochs)]
    y = losses
    ax.plot(x, y)
    plt.show()
