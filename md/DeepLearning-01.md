---
title: Deep Learning 学习笔记 01 - Overview
date: 2021-03-08 16:47:51
tags: []
categories: 学习笔记
---

写在前面：
- Q: 我为啥突然写这个呢？
- A: 因为作业要写某一讲的中文笔记，我就顺便全写成blog了。

//由于是学习笔记，所以难免有错，可能还加了私货，发现问题请指出


### 什么是深度学习(Deep Learning)？

人工智能(AI, Artificial intelligence)是一个范围很大的词语，只要是人工的，人造出来的，有智能的，能做某些任务的，就可以叫做人工智能。我认为，比如一个等概率随机出石头剪刀布的程序，就能叫AI了。而近年来人工智能大热，主要是由于深度学习这种方法达到了相当强大的效果。

深度学习是一种机器学习(Machine Learning)的方法。传统的人工智能大多数都是由专业的人手动构建程序，利用一些确定的权值计算一些结果，比如专家系统(Expert system)。机器学习与众不同的地方在于它是由机器自己通过大量数据学习一些权值(weight)，这使得它的规模和能力有了质的飞跃。

深度学习是使用神经网络(neural network)来学习(learn)数据中的特征表示(representation)。深度学习的特点在于它可以很“深”，一些深度学习的网络会由几百层神经元构成，比如ResNet。用数学表示深度学习是 $y = f(NN(x;\theta))$, 其中 $x$ 是输入，$NN(x;\theta)$ 是一个神经网络，$\theta$ 是神经网络的参数，$NN$ 的输出是一些特征表示，是一个向量。$f$ 将这个向量映射到输出 $y$。

不同于浅层学习，深度学习有大量隐藏层(hidden layer)，也是就是有除了输入的特征(feature)和输出之外的节点。这里浅层学习(shallow learning)指 $y = f(\phi(x))$, $\phi(x)$ 是人工给的特征。

//省略若干故事

### 什么是神经元(neuron)？ 感知机(Perceptron)？

直接说结果，神经元一般来说就是 $y = \sigma(\sum_i w_ix_i + b)$。$x_i$ 是这个神经元的输入，可以包括网络的输入和其他神经元的输出。$w_i$是权值，$b$ 是bias。$\sigma$ 是非线性的激活函数，常见的有sigmoid, tanh, ReLU等。如果没有 $\sigma$, 那么整个神经元就是一个线性变化，整个网络就能被一层的浅层学习表示。

感知机中的激活函数是一个阈值函数(threshold function)，`x > t ? 1 : 0`。

可能? 是出于并行加速的考虑等，神经元会被设计成一层一层的样子，每一层的神经元的输入是前一层的输出。第一层是整个网络的输入，最后一层是整个网络的输出。

看起来神经网络的层数越多，神经网络就越厉害，但是有这样一个定理：
- 两层的感知机能表示所有布尔函数
- Two-layered MLPs are universal Boolean functions

这个定理里，布尔函数是一系列 $\{0,1\}^n \rightarrow \{0,1\}$ 的函数。第一层神经元可以把一些线性约束AND起来，表示任意的凸包，第二层可以将这些凸包OR起来，表示最终的结果，但是对于XOR函数，这个网络需要 $O(2^{n-1})$ 个神经元。

但是更深的网络只需要更少的神经元。Depth-k circuits require size $\exp( \Omega(n^{1/(k-1)})) $. (Håstad, 1987)

所以深度学习要深。

//省略若干故事 (AI winter)

### 可导 (Differentiable)

感知机使用阈值函数不可导，这导致了感知机只能学到线性可分的数据，收敛速度和分开结果的两个超平面的距离有关。

使用sigmoid, tanh, ReLU等可导的激活函数后，我们可以定义一个损失函数(loss function)，表示网络的输出与我们希望得到的输出的差距（也要可导），通过梯度下降(gradient decent)，即 $\theta := \theta - \eta \frac{\partial L}{\partial \theta}$ 来更新参数。其中 $\eta$ 是学习率(learning rate)，是一个超参数(hyperparameter)，$L$ 是损失函数的输出(loss)。当整个网络凸(convex)并且光滑(smooth)的时候，有很好的收敛的界。当网络非凸时，使用加入了随机性的随机梯度下降(SGD, Stochastic gradient descent)也可以很好的收敛到一个局部最优解上（注意鞍点、极大值、不好的极小值）。

为了高效的计算深度神经网络的 $\frac{\partial L}{\partial \theta}$，现在普遍使用反向传播(Backpropagation)。就是从输出层往输入层一层一层算梯度，同时记录下最终的loss关于每一层的输出的梯度。算$\frac{\partial L}{\partial \theta}$的时候只需要下一层的梯度和当前层的输入。

对于神经网络中其他的层，比如池化(pooling)，也是用类似的方式计算。

//省略若干故事

//省略Coding Time
