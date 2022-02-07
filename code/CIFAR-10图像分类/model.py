# -*- coding: utf-8 -*-
"""
@Time    ： 2022/1/19 21:05
@Auth    ： liuhy
@File    ： model.py
@PROJECT ： lhy-nlp 
@Motto   ： ABC(Always Be Coding)

"""
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.fc1 = nn.Linear(32 * 32 * 3, 1000)
        self.fc2 = nn.Linear(1000, 500)
        self.fc3 = nn.Linear(500, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
