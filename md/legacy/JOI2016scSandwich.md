---
title: JOI2016合宿 サンドイッチ
date: 2018-01-26 18:45:13
tags: [贪心]
categories: joi
mathJax: true
---

### 题目大意

> 你有一个$n*m$的网格图，每一格为`N`或`Z`，其中`N`能被取走，当且仅当上右被取走或下左被取走，`Z`能被取走，当且仅当上左被取走或下右被取走。问每一格最早什么时候被取走。
>
> $n,m\le 400$

### 题解

第一眼以为是神仙性质题，结果标算啥性质没用，简直。。

考虑某一格，不妨设为`N`，先考虑最终是因为上右两格被取走而取走的情况。则上右两格被取走的情况确定了，使用dfs可以方便地求出它的答案，其他情况类似。复杂度$O(n^4)$。

然后使用bitset优化一波可以达到$O(\frac{n^4}{\omega})​$。

发现对于第$i$行第$j$列，最终因为上面被取走而被取走的情况，第$i-1$行第$j$列也是因为上面被取走而被取走的。按列枚举，在之前dfs跑出来的数据上dfs即可。复杂度$O(n^3)$。

不清楚是不是还有更加强的方法，比如$O(\frac{n^3}{\omega})$这种，感觉可以再多想想。。。

### 实现

```
#include<bits/stdc++.h>
#define N 405
#define inf (n*m*10)
using namespace std;
int n,m,a[N][N],b[N][N],c[N][N],now;
char s[N];
void dfs(int x,int y,int d)
{
	if (!x||!y||x>n||y>m) return;
	if (b[x][y]==-1){now=inf;return;}
	if (b[x][y]) return;
	now++;b[x][y]=-1;
	if (a[x][y])
		if (d==1||d==2) dfs(x,y-1,2),dfs(x+1,y,1);
		else dfs(x,y+1,4),dfs(x-1,y,3);
	else
		if (d==1||d==4) dfs(x,y+1,4),dfs(x+1,y,1);
		else dfs(x,y-1,2),dfs(x-1,y,3);
	b[x][y]=1;
}
int main()
{
	scanf("%d%d",&n,&m);
	for (int i=1;i<=n;i++)
		for (int j=1;j<=m;j++)
		{
			char c=getchar();
			while(c!='N'&&c!='Z')c=getchar();
			a[i][j]=c=='N';
		}
	for (int i=1;i<=n;i++)
	{
		now=0;
		memset(b,0,sizeof b);
		for (int j=1;j<=m;j++)
		{
			dfs(i,j,2);
			c[i][j]=now;
		}
	}
	for (int i=1;i<=n;i++)
	{
		now=0;
		memset(b,0,sizeof b);
		for (int j=m;j>=1;j--)
		{
			dfs(i,j,4);
			c[i][j]=min(c[i][j],now);
		}
	}
	for (int i=1;i<=n;i++)
	{
		for (int j=1;j<=m;j++)
			printf(j==m?"%d\n":"%d ",c[i][j]<inf?c[i][j]*2:-1);
	}
}

```
