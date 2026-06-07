---
title: Deep Learning 学习笔记 04 - Energy-Based Model
date: 2021-03-28 12:31:09
tags: []
categories: 学习笔记
---

之前的监督学习都是找一个网络 $f(X)$ 去预测 $y$。如果需要反过来生成 $X$ 就不行了。

要解决这个问题，我们需要使用生成模型(Generative Model)。生成模型不像监督学习学输入X和标签y的关系，而是学习输入X和标签y的联合分布(joint distribution)，$P(X,y)$ 或者 $P(X|y)$ 或者 $P(X)$。

接下来的几课会主要讲生成模型。这一课我们先来学习基于能量的模型(Energy-Based Model)。

前置知识：马尔可夫链蒙特卡洛方法(MCMC)。

### Hopfield Network

之前讲的神经网络结构都是一个DAG，那么如果我们允许神经元的连接出现环会怎么样呢？

考虑一个简化的模型。有 $n$ 个点的带权有向完全图，每个点有一个值 $y_i=\pm1$。假设边权对称，即 $w_{ij}=w_{ji}$。设定转移方程 $y_i := \Theta(\sum_{i\ne j} w_{ij}y_j + b_i)$，其中 $\Theta(x)$ 当 $x>0$ 时为 $1$，否则为 $-1$。(假设 $\sum_{i\ne j} w_{ij}y_j + b_i)\ne 0$。)

这就是Hopfield Network。

接下来，我们证明对于这种网络，不断地用这个转移方程更新 $y$，能够收敛。

定义 $D(y_1,y_2,...,y_N) = \sum_{i < j} y_iw_{ij}y_j + \sum_i y_i b_i$。假设某一步把 $y^-$ 更新成了 $y^+$，那么 $y^- (\sum_{i\ne j} w_{ij}y_j + b_i) < 0$，$y^+ (\sum_{i\ne j} w_{ij}y_j + b_i) > 0$。

$$
\Delta D = D(...,y^+,...) - D(...,y^-,...) = y^+\left (\sum_{i\ne j} w_{ij}y_j +b_i\right) - y^-\left(\sum_{i\ne j} w_{ij}y_j +b_i\right) > 0
$$

这个 $D$ 有上界，然后 $\Delta D$ 最小值大于零，就收敛了。（如果一次更新多个y的话，也是收敛的

我们称Hopfield Network的一次转移为演化(evolution)。

定义能量(energy)$E = -D$，这个网络就像一个物理系统，演化之后到达（局部）最小能量的稳定的状态。

这就很好，如果我想要存的东西正好是这个网络的一个极小值，那我就算 $y$ 有一点扰动，也可以恢复。

那么我们怎么训练这个网络呢？有一个Hebbian Learning Rule，就是对于我们想要存的模式(patten) $y$，让 $w_{ij}:=y_iy_j$，$b_i$ 直接简化掉不要。这个时候的 $E=-\frac12N(N-1)$ 是最小的。

如果要存多个patten，我们当然可以让 $w_{ij}$ 是 $\frac1N \sum_{k=1}^N y^k_iy^k_j$，但是这样会出现不好的效果，比如假的(spurious)部最小值。想要解决这个问题，可以考虑机器学习中最优化的方法。

#### 最优化(Optimization)

首先用矩阵形式化地表示Hopfield Network。对于我们希望记录的模式 $P=\{y^p\}$，我们希望找一个能量函数 $E(y) = -\frac12y^T Wy$。出于简化，我们忽略偏差值(bias) $b$。

首先我们要的不是 $\arg\min_{W}\sum_{y\in P} E(y)$，否则容易直接学成 $W=+\infty \times I$ 啥的。

一个朴素的想法是 $\arg\min_{W}\sum_{y\in P} E(y)-\sum_{y'\notin P} E(y')$，然后梯度下降 $W^{k+1} := W^k - \eta(\sum_{y\in P}yy^T-\sum_{y'\notin P}y'y'^T)$。

但是这样以来，我们需要让选的 $y'$ 数量上和 $|P|$ 相当，否则会学出 $W = -\infty \times I$ 啥的。

一个比较好的办法是对于$y\in P$，以 $y$ 为初始值，在Hopfield Network上演化几步得到 $y'$。

#### SGD Optimization

既然可以GD，那也能SGD。

### Stochastic Hopfield Network

理论上一个有 $N$ 个节点的Hopfield Network可以存 $O(N)$ 个模式。想要存更多的模式，就需要更大的网络。

以图像为例，Hopfield Network中，每个$y_i$都表示一个像素。想要扩容网络，就需要加一些冗余的神经元，或者叫隐藏(hidden)神经元。

那么新加隐藏神经元的值该怎么给呢？

一种可能的解决方法是随机赋值。但是这并不那么符合生成模型拟合概率分布的想法。

事实上，当我们有了能量函数之后，我们可以做任何事情。回忆物理上的玻尔兹曼分布，我们可以设定状态 $y$ 的概率是 $P(y) = \frac1Z\exp(-E(y)/kT)$。其中 $k$ 是一个常数，直接取1好了。$T$ 是温度。温度越高，这个概率分布越平坦，温度越低，这个概率分布趋向于在能量最大的地方取1。

众所周知，我们可以用Gibbs Sampling随机采样。在确定 $y$ 的其他位置的前提下，$y_i$ 的概率分布是
$$
P(y_i|y_{i\ne j}) = \frac{1}{1 + \exp(-(\sum_j w_{ij}y_j + 2b_i)/T)}.
$$

接下来，我们可以利用退火(Annealing)来得到这个最小能量的 $y$。具体的做法是，一开始 $T=T_{\max}$，$y$ 是随机初始化的值。然后每一轮，我们先进行若干步Gibbs Sampling，然后让 $T:=\alpha T$。若干轮后收敛。

#### 最大似然学习(maximum likelihood learning)

接下来我们来训练Stochastic Hopfield Network。

假设 $T=1$，某个特定模式 $y$ 的概率是 
$$
P(y)= \frac{\exp(\frac12 y^TWy)}{\sum_{y'} \exp(\frac12 y'^T W y')}.
$$

我们要最大化似然(likelihood)
$$
L(W) = \frac{1}{|P|} \sum_{y\in P} \frac{1}{2}y^TWy - \log \sum_{y'}\exp(\frac12 y'^TWy').
$$

$$
\nabla_{w_{ij}}L(W) = \frac{1}{|P|} \sum_{y\in P} y_iy_j - \frac{1}{Z}\sum_{y'} \exp(\frac12 y'^TWy')y_i'y_j'
$$

由于 $y'$ 的数量是指数级的，后面 $\log \sum_{y'}\exp(\frac12 y'^TWy')$ 的梯度不好算。我们需要按照概率随机采样来估计这个梯度。设随机的样的集合是$\mathcal S$，
$$
\nabla_{w_{ij}}L(W) := \frac{1}{|P|} \sum_{y\in P} y_iy_j - \frac{1}{|\mathcal S|} \sum_{y' \in \mathcal S} y_i'y_j'.
$$

这里对 $y'$ 采样也可以像Hopfield Network上一样，从 $y\in P$ 出发跑几步Gibbs sampling。

#### 隐藏神经元(with Hidden Neurons)

用Stochastic Hopfield Network可以很好处理隐藏神经元。

设对于一个状态 $y=(v,h)$，可见神经元的值是 $v$，隐藏神经元的值是 $h$。可见神经元就是能看到的部分，比如存一张图片，图片自己的像素就是可见的。

$$
P(v) = \sum_h P(v,h) = \sum_{y = (h,v)} \frac{\exp(\frac12 y^TWy)}{\sum_{y'} \exp(\frac12 y'^T W y')}
$$

$$
L(W) = \frac{1}{|P|} \sum_{v\in P}\log\left( \sum_{y=(v,h)}\exp(\frac{1}{2}y^TWy)\right) - \log \sum_{y'}\exp(\frac12 y'^TWy').
$$

前面这项的 $h$ 的数量也是指数级的，可以用和之前类似的方法（Gibbs Sampling）按照概率随机采样。

$$
\nabla_{w_{ij}}L(W) := \frac{1}{|P|} \sum_{v\in P} \mathbb E_{h}[y_iy_j] - \mathbb E_{\mathcal S} [y_i'y_j'].
$$

如果想要再加一个标签 $c$，得到 $P(v|c)$，就让 $y=(v,h,c)$，然后最大似然学习。

### 受限玻尔兹曼机(Restricted Boltzmann Machine)

Stochastic Hopfield Network确实厉害，而且有一套很好的理论性质，但是它是建立在Gibbs Sampling上的。Gibbs Sampling虽然可以做到多项式时间的采样，但是仍然需要多轮之后才能趋向平稳分布(stationary distribution)，尤其是在训练的过程中，有两个需要采样的项。

于是有了受限玻尔兹曼机。与Hopfield Network不同，受限玻尔兹曼机只在隐藏神经元与可见神经元之间连边，隐藏神经元与隐藏神经元之间、可见神经元与可见神经元之间不连边。

回顾Gibbs Sampling，每次选一个维度随机选。在受限玻尔兹曼机上，由于这样的连边，我们可以同时让所有隐藏神经元或者所有可见神经元一起随机。

于是在 $v$ 的条件下，对 $h$ 采样就只需要一轮。对 $y'$ 的采样可以从 $v$ 生成 $h$，然后生成 $v_1$， 然后生成 $h_1$，用 $y'=(v_1,h_1)$ 来代替收敛后的 $y'$。这相当于Hopfield Network里，只增加模式附近的能量。

这玩意儿只要3次Gibbs sampling，终于能够用于实践了。

然后这玩意儿的隐藏层可以叠好多层，相邻的层之间有连边，就是Deep Boltzmann Machine。

//Hinton 牛逼（

### 一般的基于能量的模型

一般的基于能量的模型是先学出一个能量函数 $E(x:\theta)$，然后 $P(x) = \frac1Z \exp(E(x))$，其中 $Z$ 是归一化系数。

计算 $Z$ 的难度非常大。那么有没有办法避免 $Z$呢？

我们可以每次找一个正例 $x$ 和一个反例 $x'$，$P(x)/P(x') = \exp(E(x) - E(x'))$。

想要从这个模型中采样，首先随机初始化一个 $s^0$，然后每一轮给它加个噪声 $s' = s^i + \epsilon$，如果加了之后能量变大了，就跳过去，否则以 $\exp(E(s^i)-E(s^{i+1}))$ 跳过去。（Metropolis-Hasting）

