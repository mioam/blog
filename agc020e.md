---
title: agc020E - Encoding Subsets
date: 2018-01-17 15:01:16
tags: [搜索]
categories: atcoder
---


### 题目大意

> 一个01串，可以使用以下方法表示：
> - $0$和$1$分别可用$0$和$1$表示
> - 如果$A$,$B$分别可用$P$,$Q$表示，则$A+B$可用$P+Q$表示。
> - 如果$A$可用$P$表示，则$AA...A$（$K$个）可用$(P*K)$表示
> 
> 现在问一个长为$S$的串$A$，所有的$B\in A$共有几种表示方式。
>
> $n\leq5000 ,\sum s_i\leq2*10^6$

### 题解

考虑$f(x)$表示$x$这个串的答案，$g(x)$表示$x$这个串分成$(P*K)$的方案数。然后使用记忆化搜索发现可以过。
考虑复杂度上界都能够表示为$A$中某一段中的某一段重复若干次的交，大概为$O(玄学)$种不同的串，反正用dp算的复杂度是对的。

### 实现

```
#include<bits/stdc++.h>
#define P 998244353
#define ll long long
using namespace std;
map<vector<int>,int>mp,pm;
int Get(vector<int> S);
int G(vector<int>S)
{
	int n=S.size();
	if (n==1) return S[0]?2:1;
	if (mp[S]) return mp[S];
	int sum=0;
	for (int i=2;i<=n;i++)
	if (n%i==0)
	{
		vector<int>tmp;tmp.clear();
		for (int j=1;j<=n/i;j++)
			tmp.push_back(1);
		for (int j=0;j<n;j++)
			tmp[j%(n/i)]&=S[j];
		//cout<<tmp[0]<<' '<<S[0]<<endl;
		sum=(sum+Get(tmp))%P;
	}
//	cout<<"#";for (int i:S)cout<<i<<' ';cout<<sum<<endl;

	return mp[S]=sum;
}
int Get(vector<int> S)
{
	if (pm[S]) return pm[S];
	int n=S.size(),sum=G(S);
	vector<int>T;T.clear();
	for (int i=1;i<n;i++)
	{
		T.push_back(S[i-1]);
		vector<int> tmp;tmp.clear();
		for (int j=i;j<n;j++)tmp.push_back(S[j]);

		sum=(sum+(ll)G(T)*Get(tmp))%P;
	}
//	for (int i:S)cout<<i<<' ';cout<<sum<<endl;
	return pm[S]=sum;
}
int main()
{
	int n;char s[1005];
	scanf("%s",s+1);n=strlen(s+1);
	vector<int>S;
	for (int i=1;i<=n;i++)
		S.push_back(s[i]-'0');
	printf("%d\n",Get(S));
}
```