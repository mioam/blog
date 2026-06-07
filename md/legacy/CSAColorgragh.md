---
title: csacademy Colorgragh
date: 2018-01-04 07:38:15
tags: [网络流,图论]
categories: csacademy
mathJax: true

---

### 题目大意

> 给出一张有$n$的节点的有向完全图，每一条边有0,1两种颜色。对于这样的图，可以使用数对$(A,B)$来描述，$A$表示只考虑0边是否连通，$B$表示只考虑1边是否连通。
> 现在你可以选择若干条边，使上面的颜色取反，问最少操作几次可以使原图可以使用给定的数对$(A,B)$来描述。需要输出方案。
>
> $3\leq n\leq250$

### 题解

首先考虑$A=B=0$的情况，显然必定无解。

 - 考虑1边不连通，则原图至少可以分成两个部分，所有端点不在同一部分中的边都是0边，此时0边连通。

在此基础上$A+B=1$的情况就相当于求一种边的无向图最小割，显然这个时候另一种边连通。使用$stoer-wagner$算法可以做到$O(n^3)$以内。

然后考虑$A=B=1$的情况。当$n>3$时才有解。不妨假设初始时1边不连通。那么答案至少为只考虑1边的连通块个数-1。
现在尝试构造出等于这个下界的解：

- 对于连通块$X,Y$，若$|X|>1$且$|Y|>1$，则任选一条连接$X,Y$的边变为1即可使他们连通，同时不改变0边的连通性。
- 对于大小为$1$的连通块$s$，选择一条相邻的0边反色，当他的另一个顶点$a$有至少一条相邻的0边$a$->$b$，通过这条边，$a$与$b$，$b$与$s$，$s$与其他点通过0边相连。
- 当存在超过$2$个连通块时，对每个大小为$1$的连通块必然存在这样的0边。
- 当只有两个连通块，且其中一个大小为$1$的情况下可以证明下界为$2$，并且容易构造方案。

这部分复杂度可以做到$O(n)$。
所以$n$是可以出到$500$的。
另外题目中需要忽略自环，并且其中一组数据多了一个$s$,需要使用读入优化。

### 实现

```
#include<bits/stdc++.h>
#define N 255
using namespace std;
int n,a[N][N],vis[N],cnt;
vector<int>v[N];
struct T
{
	int x,y;
}b[N],Ans[N*N];
bool cmp(T a,T b)
{
	return a.y<b.y;
}
void dfs(int x,int y)
{
	vis[x]=1;cnt++;
	for (int i=1;i<=n;i++)
		if (!vis[i]&&a[x][i]==y) dfs(i,y);
}
int check(int x)
{
	cnt=0;
	memset(vis,0,sizeof vis);
	dfs(1,x);
	return cnt==n;
}
void Dfs(int x)
{
	vis[x]=1;v[cnt].push_back(x);
	for (int i=1;i<=n;i++)
		if (!vis[i]&&a[x][i]) Dfs(i);
}
int c[N],fa[N],w[N],ha[N][N];
int Get(int x)
{
	return fa[x]==x?x:fa[x]=Get(fa[x]);
}
int read()
{
	int x=0;char c=getchar();
	while(c<'0'||c>'9')c=getchar();
	while(c>='0'&&c<='9')x=x*10+c-'0',c=getchar();
	return x;
}
int main()
{
	n=read();
	for (int i=1;i<=n;i++)
	{
		for (int j=1;j<=n;j++)
			a[i][j]=read();
		a[i][i]=0;
	}
	int A,B;
	A=read();B=read();
	if (A==0&&B==0)puts("-1");
	else if (A+B==1)
	{
		if (!A)
		{
			swap(A,B);
			for (int i=1;i<=n;i++)
				for (int j=1;j<=n;j++)
					if (i!=j) a[i][j]^=1;
		}
		if (!check(1))
			puts("0");
		else
		{
			//1的最小割 
			int Mn=n*2;
			for (int i=1;i<=n;i++)
				for (int j=1;j<=n;j++)
					ha[i][j]=a[i][j];
			
			for (int i=1;i<=n;i++)
				fa[i]=i;
			for (int i=1;i<n;i++)//n-1次缩点  
			{
				memset(w,0,sizeof w);
				memset(vis,0,sizeof vis);
				
				w[1]=0;vis[1]=1;c[0]=1;
				for (int j=1;j<=n;j++)
					if (fa[j]==j&&a[1][j])
						w[j]+=a[1][j];
				
				for (int j=1;j<=n-i;j++)
				{
					int tmp=0;
					for (int k=1;k<=n;k++)
						if (fa[k]==k&&!vis[k]&&(tmp==0||w[tmp]<w[k]))
							tmp=k;
					
					c[j]=tmp;vis[tmp]=1;
					for (int k=1;k<=n;k++)
						if (fa[k]==k&&a[tmp][k])
							w[k]+=a[tmp][k];
				}
				int u=c[n-i-1],v=c[n-i];
				if (w[v]<Mn)
				{
					Mn=w[v];
					int ly=0;
					for (int j=1;j<=n;j++)
					{
						for (int k=1;k<j;k++)
							if ((Get(j)==v&&Get(k)!=v||Get(j)!=v&&Get(k)==v)&&ha[j][k])
								Ans[++ly]=(T){j,k};
					}
				}
				if (u>v)swap(u,v);fa[v]=u;
				for (int i=1;i<=n;i++)
				{
					if (a[v][i]&&i!=u) a[u][i]+=a[v][i];
					if (a[i][v]&&i!=u) a[i][u]+=a[i][v];
				}
			}
			printf("%d\n",Mn);
			for (int i=1;i<=Mn;i++)
			{
				printf("%d %d\n",Ans[i].x,Ans[i].y);
			}
		}
		
	}
	else if (n==3)
	{
		puts("-1");
	}
	else
	{
		if (!check(0))
		{
			swap(A,B);
			for (int i=1;i<=n;i++)
				for (int j=1;j<=n;j++)
					if (i!=j) a[i][j]^=1;
		}
		//将1联通 
		cnt=0;
		memset(vis,0,sizeof vis);
		for (int i=1;i<=n;i++)
		{
			if (!vis[i])
			{
				cnt++;
				Dfs(i);
				b[cnt]=(T){cnt,(int)v[cnt].size()};
			}
		}
		sort(b+1,b+cnt+1,cmp);
		if (b[1].y>1)
		{
			printf("%d\n",cnt-1);
			for (int i=1;i<cnt;i++)
				printf("%d %d\n",v[i][0],v[i+1][0]);
		}
		else if (b[2].y>1)
		{
			if (cnt==2)
			{
				int flag=0;
				for (int i=1;i<=n&&!flag;i++)
					for (int j=1;j<=n;j++)
						if (i!=j&&i!=v[b[1].x][0]&&j!=v[b[1].x][0]&&a[i][j]==0)
						{
							flag=i;
							break;
						}
				if (flag)
					printf("%d\n%d %d\n",1,v[b[1].x][0],flag);
				else
				{
					int tmp=v[b[1].x][0];
					printf("%d\n%d %d\n%d %d\n",2,tmp,tmp%n+1,tmp%n+1,(tmp+1)%n+1);
				}
			}
			else
			{
				printf("%d\n",cnt-1);
				for (int i=1;i<cnt;i++)
				{
					printf("%d %d\n",v[i][0],v[i+1][0]);
				}
			}
		}
		else
		{
			printf("%d\n",cnt-1);
			for (int i=1;i<cnt;i++)
			{
				printf("%d %d\n",v[i][0],v[i+1][0]);
			}
		}
	}
	
}
```