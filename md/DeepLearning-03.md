---
title: Deep Learning 学习笔记 03 - Supervised Learning (2)
date: 2021-03-27 21:17:51
tags: []
categories: 学习笔记
---

//gugugu \~

前两课讲了一些深度学习的概念，讲了深度学习的网络是个啥，但是想让模型有用，我们还需要训练这个网络。

这一讲的内容很偏向实践，反正就是去试（

GET YOUR HANDS DIRTY!

### 训练（training）

上节课说到，对于训练集 $\mathcal S$，我们希望得到一组参数 $\theta^*$ 最小化网络在训练集上的损失，即 $\theta^* = \arg\min_{\theta\in \Theta} Loss_{\mathcal S}(\theta)$。但是显然，如果 $Loss_{\mathcal S}(\theta)$ 没有什么性质，这个最优化的过程是很难的。

#### 梯度下降(gradient decent)

在深度学习问题上，人们现在最常用的最优化算法是梯度下降。

简单来讲，梯度下降就是 $\theta^{i+1} = \theta^{i} - \eta \nabla Loss(\theta)$。直观理解就是首先有个初始的 $\theta^0$，然后每次把它往梯度的反方向挪一点。如果 $Loss$ 在这一点很陡就多挪一点，很平就少挪一点。感觉上这样一直挪就能减小 $Loss(\theta)$ 的值，最后收敛到一个平的地方。这个式子里的 $\eta$ 被称为学习率(learning rate)，用来决定这样挪一点的比例。具体的学习率需要通过实验得到。实践中也可以动态的修改学习率来达到更好的效果。//$\theta^i$ 指 $i$ 轮梯度下降之后的参数，不是 $i$ 次方！因为 $\theta$ 是个向量，上标用来和 $\theta_i$ 区分。

当 $Loss$ 函数凸并且“光滑”的时候，合适的学习率可以让梯度下降的结果收敛。一个感觉是，学习率很大的话，我的 $\theta$ 会跳来跳去；学习率很小的话，我的 $\theta$ 会走的很慢。

形式化的，一个函数凸，即 $f(x+y) \le \frac12(f(x)+f(y))$ 或者说 $\nabla^2 f(x) \gtrsim 0$。若 $\nabla^2 f(x) \gtrsim \mu >0$，则称这个函数 $\mu$-strongly convex。

一个函数的梯度是 $L$-Lipschitz 则称这个函数 $L$-smooth，即 $\|\nabla f(x)-\nabla f(y)\|\le L\|f(x)-f(y)\|$ 或者说 $\nabla^2 f(x) \lesssim LI$。

可以证明，当 $0< \eta < \frac2L$ 时，想要得到 $\|\nabla f(\theta)\|\le \epsilon$ 所需要的梯度下降次数是 $O(\frac1\epsilon)$。strongly convex 可以达到 $O(\log \frac1\epsilon)$。（Weight decay 相当于在 Loss 里加了一项 $\|\theta\|_2^2$，能把凸的函数变成强凸的，能够带来更好的分析上的性质(better analytical properties)。）

然而这些理论无法适用于深度学习，因为深度神经网络的 $Loss$ 相当复杂，既无法保证凸，也并不光滑(比如ReLU），或者L特别大。深度学习选择梯度下降（实际上是随机梯度下降）的比较流行的假说(hypothesis)大概是，在深度神经网络的Loss上，这个算法能够跳出鞍点和比较菜的局部最小值（或者这种点很少），并且最终能停下来的局部最小值都一样厉害。

#### 一些优化(accelerate)

上面这个梯度下降也有优化空间。可以发现，上面的梯度下降算法只用了函数的一阶梯度。你可以用牛顿法(Newton’s method)得到更快的收敛，但是算Hessian矩阵很耗时，得到Hessian的逆需要参数数量（随便百万级别以上）立方的时间，这完全无法接受。

进一步思考，只使用一阶梯度的梯度下降，
对于不同的维度上，不同方向上，不同大小的梯度，只能使用单一的学习率。我们希望在梯度变化不大的方向，学得快一点，在像一个凹槽的地方，学得慢一点。“一些SGD的改进”中详细讲了几种优化，但是我懒得写了。

实践中，我们可以用动量(momentum)来自动达到这个效果。一句话概括，$x_{i+1} = x_i - \eta \nabla f(x_i) +\beta(x_i-x_{i-1})$。相当于给了梯度下降一个惯性，有一种一个球在一个曲面上自由地滚的感觉。但是，这个最常用的形式没有理论上的收敛保证。一个改进方法是 Nesterov’s accelerated gradient descent，$x_{i+1} = x_i - \eta \nabla f(x_i + \beta(x_i-x_{i-1})) +\beta(x_i-x_{i-1})$。~~小声bb：反正最后都是玄学~~

### 随机梯度下降 SGD (Stochastic Gradient Descent)

在深度学习中，我们往往需要一个巨大的数据集。在这个数据集上完整地计算准确的梯度需要消耗很多时间，但是我们根本不需要那个准确的梯度，我们只需要找一个方向让它往哪里挪就好了。于是我们可以使用SGD。

我们每次从数据集中随机选出 $m$ 个数据，然后用这 $m$ 个数据计算梯度。（注意，如果整个数据集有 $n$ 个数据，那么Loss函数最后是 $n$ 个东西的平均。现在只有 $m$ 个数据，这 $m$ 个数据上的 Loss 就需要是 $m$ 个数的平均。这样的话，学习率可以与数据集大小无关。）这里随机选出的 $m$ 个数据被称为 mini-batch，$m$ 被成为batch-size。

实践中，我们希望每一个数据起到一样大的影响。所以一般来讲，一次训练会被分成若干epoch进行。每个epoch把数据集随机分成若干mini-batch，然后遍历这些mini-batch，进行梯度下降。这样以来，每个数据在每个epoch会被计算1次。（假设 $n$ 是 $m$ 的倍数。）

理论上，比较广义的SGD只需要每次算的梯度的期望等于真实的梯度即可，所以给GD的梯度加一个高斯噪声啥的，都可以是SGD。

在SGD中，一个重要的超参数就是batch-size。一般来说，更大的batch-size能够减小计算出的梯度的方差，能收敛的更好，所需的梯度下降的轮数会少。但是小的batch-size可以让每一轮梯度下降更快完成计算，尽管可能需要更多轮梯度下降，但是最终可能可以更快收敛。不同大小的batch-size对于模型的泛化能力(generalization)也会有一定影响。一般来说，batch-size的选择可以根据显存大小调整，取到一个mini-batch能全放进显存就挺好。你跑一些图像的深度学习，可能每次只放一个数据去训，显存就满了（

实践中，SGD可以带一个momentum。

#### 一些SGD的改进：AdaGrad，AdaDelta，RMSProp，Adam

咕 \~

~~反正Adam牛逼 //然而我的作业里最后选的没momentum的SGD~~

具体什么最优化算法需要根据网络结构、任务类型等实际情况选择。

### 一些实践中的trick

上一讲中提到了监督学习的逻辑。我们最后是要用网络去拟合一个分布。

实践中，很多时候，深度神经网络遇到的问题往往不是欠拟合(underfitting)，而是过拟合(overfitting)。也就是说，我们的网络寻到最后，往往都可以学会训练集的分布，但是在真实分布，或者测试集上的表现会差很多。比如在训练集达到99.9%正确率，但是测试集上只有80%。

实践中，我们可以先确保网络能够过拟合训练集，然后在训练过程中加入一些trick，以此增强模型的泛化能力(generalization)。

很多trick在主流的机器学习库里都有实现，用的时候直接调就好了（

#### Weight decay

“梯度下降”中提到过weight decay。Weight decay就是在每轮梯度下降之后把所有参数乘上一个小于1的系数 $w$。

这相当于在Loss函数中添加了一项 $\frac{1-w}{2}\|\theta\|_2^2$，因为这个东西对 $\theta_i$ 的导数正好是 $(1-w)\theta_i$。

类似的东西还有LASSO。

#### 数据准备和数据增强(Data Preparation and Augmentation)

用图像分类问题的AlexNet为例，数据准备大概是把图片都裁成224x224啥的。数据增强大概就是每次从训练集拿出图片的时候，加个随机翻转/随机旋转/随机擦除/随机噪声啥的。

#### Dropout ~~辍学~~ 

~~啥都学不会，只能dropout~~

Dropout在训练的时候，每轮梯度下降每个神经元有一定概率 $p$ 被关闭。被关闭的神经元在这一轮中不参与正向传播和反向传播。

在最终测试时，神经元不再会被关闭，但相应的神经元的输出需要乘 $1-p$ 使得最终输出的期望的平均值不变。

#### Early Stopping ~~提早停下~~

一般来讲，训练过程一开始validation loss和training loss会同时下降，但是在过拟合之后，validation loss会开始上升。我们可以当validation loss达到最小值时停止训练。

#### 初始化(Initialization)

最优化的初始化往往很关键。

深度学习中的初始化需要额外考虑的一个问题是：不太好的初始化很容易让网络里的值爆炸。比如某个初始化，每一层把输入乘二，$n$ 层之后，输入就会变成 $2^n$ 倍，直接超出浮点数表示范围。

所以我们往往通过合理的初始化，使得经过神经网络之后能够保持均值和方差。初始化还和激活函数有关。可以使用Xavier Initialization，或者Kaiming Initialization。

#### 预训练初始化(Pretrained Initialization)

除了随机的初始化，我们还可以用现成的网络参数来初始化。比如用表现不那么好的模型，或者类似任务上的模型等。我们可以对整个网络初始化，也可以只初始化前面的几层。我们相信这样的预训练模型能够提取一些普遍性的特征。

#### Gradient Clipping

有时候，我们算梯度还是不可避免的出现了巨大的梯度值，甚至inf。如果直接跳过去，很可能让整个网络直接学废。我们可以把梯度的绝对值和一个小常数取max。

#### Batch Normalization

Batch Normalization层 $f(x) = \gamma \frac{x-\mu}{\sqrt{\sigma^2+\epsilon}} + \beta$，把每个mini-batch的均值和方差拉成一样。

//等等等

### 进阶网络结构

Residual Network

Densely Connected Network

Deconvolution

Fully Convolutional Network (Revisited)

### Google Colab 使用教程

咕 \~
