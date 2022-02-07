### 问题描述

最近做模型训练的时候，我发现在每个训练batch中都需要调用一下optimizer.zero_grad()方法。 why???

### 探索
先解释一下这个方法的作用：很简单其实就是将模型中参数的梯度设置为0；

那问题来了为什么要将梯度设置为零呢？

根据pytorch中的backward()函数的计算，当网络中的参数进行backprop时，梯度是被积累的而不是被替换掉；但是在训练每一个batch时毫无疑问并不需要将前后两个batch的梯度混合起来累积，因此这里就需要每个batch设置一遍zero_grad 了。
这样每次训练新的batch时参数优化的梯度都是当前batch自己的梯度。

### 思考
了解了zero_grad的原理和作用那免不了又冒出来一个奇怪的想法，既然梯度在不同batch之间是累计的，那么是不是可以训练两个甚至是3个batch之后（此时gradient已经积累3个batch了）再进行参数的调整，这样实际上是变相的增加了batch_size，这种方式适合于计算机硬件不行但是还必须需要设置较高的batch_size的情况（听大佬说目标检测的模型训练就属于这个情况）。

注：
参考：https://discuss.pytorch.org/t/why-do-we-need-to-set-the-gradients-manually-to-zero-in-pytorch/4903/3

https://discuss.pytorch.org/t/how-to-use-the-backward-functions-for-multiple-losses/1826/5

https://blog.csdn.net/PanYHHH/article/details/107361827?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.pc_relevant_paycolumn_v2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.pc_relevant_paycolumn_v2&utm_relevant_index=2