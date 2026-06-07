---
title: JOI2016合宿 回転寿司
date: 2018-01-22 12:41:00
tags: [分块]
categories: joi
---

### 题目大意

> 现在$n$个人逆时针坐成一圈。起初每个人都有一个费用为$X_i$的盘子。
> 由于店家促销，接下来$Q$次操作，在$S_i$放一个费用为$P_i$的盘子。这个盘子会在传送带上逆时针移动到$T_i$。若一个人当前的费用大于面前的盘子，就会交换这两个盘子。
> 现在对于$Q$个操作，输出最后回收的盘子的费用。
> 
> $n<=400000，m<=25000$

### 题解

考虑分块。对于每个块维护一个堆，每次一个盘子从左边进入后加入堆，最后将堆顶弹出。对于不是整块的询问，需要还原某个块的真实情况，发现相当于把原有的盘子放到操作序列中，相当于一个$S_i=1,T_i=n$的原问题，容易完成。复杂度$O(n\sqrt{n}log(n))$。

由于一些偏差，我一开始考虑将非整块的子问题递归处理，复杂度为$T(n,q)=qT(q,sz)+nqlog(n)/sz$，然后发现没有然后了。。但是或许换个题目就无敌了。~~所以有没有大神来一道毒瘤题啊~~

### 实现

```
#include<bits/stdc++.h>
#define N 400005
using namespace std;
int n,Q,a[N],SZ,bl[N];
priority_queue<int>q[1005],v[1005];
void rebuild(int x)
{
	int l=x*SZ+1,r=min(n,(x+1)*SZ);
	for (int i=l;i<=r;i++)
	{
		q[x].push(-a[i]);
		a[i]=-q[x].top();
		q[x].pop();
	}
	while(q[x].size())q[x].pop();
}
void build(int x)
{
	int l=x*SZ+1,r=min(n,(x+1)*SZ);
	while(v[x].size())v[x].pop();
	for (int i=l;i<=r;i++)
		v[x].push(a[i]);
}
int mdy(int s,int t,int p)
{
	for (int i=s;i<=t;i++)
		if (p<a[i])swap(a[i],p);
	return p;
}
int Mdy(int s,int t,int p)
{
	if (bl[s]==bl[t])
	{
		rebuild(bl[s]);
		p=mdy(s,t,p);
		build(bl[s]);
	}
	else
	{
		rebuild(bl[s]);
		rebuild(bl[t]);
		p=mdy(s,min(n,(bl[s]+1)*SZ),p);
		for (int i=bl[s]+1;i<bl[t];i++)
		{
			q[i].push(-p);
			v[i].push(p);
			p=v[i].top();
			v[i].pop();
		}
		p=mdy(bl[t]*SZ+1,t,p);
		build(bl[s]);
		build(bl[t]);
	}
	return p;
}
int main()
{
	scanf("%d%d",&n,&Q);
	SZ=sqrt(n)+1;
	for (int i=1;i<=n;i++)
	{
		scanf("%d",&a[i]);
		bl[i]=(i-1)/SZ;
		v[bl[i]].push(a[i]);
	}
	while(Q--)
	{
		int s,t,p;
		scanf("%d%d%d",&s,&t,&p);
		if (s>t) p=Mdy(1,t,Mdy(s,n,p));
		else p=Mdy(s,t,p);
		printf("%d\n",p);
	}
}

```