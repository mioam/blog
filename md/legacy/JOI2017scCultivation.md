---
title: JOI2017合宿 開拓
date: 2017-12-27 19:22:06
tags: 
categories: joi
mathJax: true
---

### 题目大意

>  给出一张$R*C$的图，一开始上面有$n$颗草。每个时刻可以刮一个方向（东南西北）的风，然后所有草向那个方向拓展一格，求覆盖整张图的最小时间。
>
> $n\leq 100$，$R,C\leq1e9$

### 题解

首先发现刮风的顺序不重要，可以枚举每个方向风的总时间，$O(R^3C^3)$。
然后考虑优化，不妨将所有草向左平移直到第一列有草，显然答案不变。然后考虑只枚举东风和西风，之后算出每一列至少需要$a$个南风，$b$个北风，$c$个风，答案就是$max(max_a+max_b,max_c)$。

先考虑西风，可以看做把一个东风变成西风，然后向右平移整张图，于是可以只枚举东风，然后在此基础上统计区间的$max_a,max_b,max_c$。由于不同的列只有$O(n)$种，这部分可以使用set维护当前列的状态做到$O(C^2logn)$或$O(Cnlogn)$。

接下来发现有用的东风只有$O(n^2)​$种，即对任意两个草即将追上的东风与在最终平移之后的途中分别为左右端点的东风以及不吹东风。至此复杂度为$O(n^3logn)​$。

但是由于常数较大，这样无法通过$subtask5,6$。发现确定东西风的和之后，统计每一列的$a,b,c$可以$O(n^3)$预处理。具体的，可以将草按列坐标排序，用$f_{i,j}$记录第$i$~$j$颗草都覆盖到的某列的$a,b,c$。统计区间$max$的部分利用单调队列可以做到$O(n)$。所以在$O(n^3)$时间内完成了答案的计算。

### 实现

```
#include<bits/stdc++.h>
#define N 305
#define ll long long
#define inf 3000000000
using namespace std;
int b[N*N*3],e[N];ll c[N*2];
int R,C,n,cnt;ll Ans,W1;
struct T
{
	ll x,y,z;
}pre[N][N];
struct T1
{
	ll x,y;
}a[N];
struct Tp
{
	ll x,y,a,b,c;
}d[N*2];
bool cmp1(T1 a,T1 b){return a.y<b.y;}
bool cmp2(int x,int y){return a[x].x<a[y].x;}
struct pq
{
	T1 q[N*2];int l,r;
	void clr(){l=1;r=0;}
	void push(T1 x){while(r>=l&&q[r].x<=x.x) r--;q[++r]=x;}
	void pop(ll y){while(l<=r&&q[l].y<y)l++;}
	ll top(){return q[l].x;}
}na,nb,nc;
void work(ll tmp)
{
	//if (tmp>=Ans) return;
	int hz=0,ly=1,i,j,l,r;
	c[1]=1;
	for (i=1,j=1;i<=n||j<=n;)
	{
		if (i<=n&&(j>n||a[i].y<a[j].y+tmp+1)) c[++ly]=a[i++].y;
		else c[++ly]=a[j++].y+tmp+1;
	}
	c[ly+1]=inf;
	for (j=1,l=1,r=1;j<=ly;j++)
		if ((j==ly||c[j]!=c[j+1]))
		{
			while(l<=n&&a[l].y+tmp<c[j])l++;
			while(r<=n&&a[r].y<=c[j])r++;
			if (l>=r) d[++hz]=(Tp){c[j], c[j+1]-1,inf,inf,inf};
			else d[++hz]=(Tp){c[j], c[j+1]-1,pre[l][r-1].x,pre[l][r-1].y,pre[l][r-1].z};
		}
	na.clr();nb.clr();nc.clr();
	for (i=1,j=1;i<=hz;i++)
	if (d[i].x-1<=tmp&&d[i].x!=d[i-1].x)
	{
		ll l=d[i].x,r=d[i].x-1+C;
		while(j<=hz&&d[j].x<=r)
		{
			na.push((T1){d[j].a,d[j].y});
			nb.push((T1){d[j].b,d[j].y});
			nc.push((T1){d[j].c,d[j].y});
			j++;
		}
		na.pop(l);nb.pop(l);nc.pop(l);
		//if (na.top()>=inf||nb.top()>=inf||nc.top()>=inf)continue;
		Ans=min(Ans,max(na.top()+nb.top(),nc.top())+tmp);
	}
}
int main()
{
	scanf("%d%d%d",&R,&C,&n);Ans=R+C;
	W1=C;
	for (int i=1;i<=n;i++)
	{
		scanf("%lld%lld",&a[i].x,&a[i].y);
		W1=min(W1,a[i].y);e[i]=i;
	}
	for (int i=1;i<=n;i++)
		a[i].y-=W1-1;
	sort(a+1,a+n+1,cmp1);
	sort(e+1,e+n+1,cmp2);
	for (int i=1;i<=n;i++)
	{
		for (int j=i;j<=n;j++)
		{
			ll now=0,na=0,nb=0,nc=0;
			for (int k=1;k<=n;k++)
				if (e[k]>=i&&e[k]<=j)
				{
					if (!now) na=a[e[k]].x;
					else nc=max(nc,a[e[k]].x-now);
					now=a[e[k]].x;

				}
			nb=R-now;
			pre[i][j]=(T){na-1,nb,nc-1};
		}
	}
	for (int i=1;i<=n;i++)
	{
		for (int j=1;j<=n;j++)
		{
			if (a[i].y<a[j].y)
			{
				//b[++cnt]=a[j].y-a[i].y;
				b[++cnt]=a[j].y-a[i].y-1;
			}
			b[++cnt]=C+a[j].y-a[i].y-1;
		}/*
		b[++cnt]=C-a[i].y;
		b[++cnt]=a[i].y-1;*/
	}
	b[++cnt]=0;
	b[++cnt]=C-1;
	sort(b+1,b+cnt+1);
	for (int i=1;i<=cnt;i++)
		if (i==1||b[i]!=b[i-1])
			work(b[i]);
	printf("%lld\n",Ans);
}
```
