# 稳定匹配问题

1962年，盖尔（David Gale）和沙普利（Lloyd Shapley）首次提出了稳定匹配婚姻问题，这个问题也是研究该类型问题的典型。可以利用舞伴问题来一窥**Gale-Shapley算法**的奥妙。

舞伴问题：有n个男孩与n个女孩参加舞会，每个男孩和女孩均有一个按照自己偏爱程度排序的中意舞伴名单，排在最前面的是最中意的舞伴。问：是否可以将他们分成稳定的n对，使每个人都能和他们中意的舞伴跳舞？

## 1. 算法原理

Gale-Shapley算法的策略是一种寻找稳定婚姻的策略，该策略不管男女之间有何种偏好，总可以得到一个稳定的婚姻匹配。

稳定匹配包含2层意思：

> 1. 首先，它是一个完美匹配
> 2. 其次，它不包含任何不稳定因素

Gale-Shapley算法实现的伪代码：

> 初始化所有的m $\in$ M ，w$\in$W，所有的m和w都是自由状态；
>
> while( 存在男人是自由的，并且他还没有对每个女人都求过婚 )
>
> {
>
> ​	选择一个这样的男人；
>
> ​	w = m 的优先选择表中还没有求过婚的排名最高的女人；
>
> ​	if（w是自由状态）
>
> ​	{
>
> ​		将（m，w）的状态设置为约会状态；	
>
> ​	}
>
> ​	else
>
> ​	{
>
> ​		m' = w当前约会的男人；
>
> ​		if(w更喜欢m'而不是m)
>
> ​		{
>
> ​			m不变；
>
> ​		}
>
> ​		else
>
> ​		{
>
> ​			将（m，w）的状态设置为约会状态；
>
> ​			将m'设置为自由状态；
>
> ​		}
>
> ​	}
>
> }

## 2. 算法实现

首先定义舞伴的数据结构。

```c++
typedef struct tagPartner
{
    char *name;   //名字
    int next;     //下一个邀请对象
    int current;  //当前舞伴，-1表示还没有舞伴
    int pCount; //偏爱列表中舞伴个数
    int perfect[UNIT_COUNT]; //偏爱列表
}PARTNER;
```

使用数组来存储男孩和女孩列表，因此，上述数据结构中的next、current和perfect列表中存放的都是数组索引。

将小节1中的伪代码翻译为编程语言即可。

```c++
/* 返回舞伴在自己偏爱列表中的位置，用来判断女孩喜欢的一个舞伴的程度，返回值越小，越喜欢*/
int GetPerfectionPosition( PARTNER *partner, int id )
{
    for( int i = 0; i < partner->pCount; i++)
    {
        if(partner->perfect[i] == id ) 
            return i;        
    }
    return 0x7FFFFFFF;
}

bool Gale_Shapley( PARTNER *boys, PARTNER *girls, int count )
{
    int bid = FindFreePartner( boys, count ); // 选择一个男孩
    while ( bid >= 0 )
    {
        int gid = boys[bid].perfect[boys[bid].next];
        if ( girls[gid].current == -1 )
        {
            boys[bid].current = gid;
            girls[gid].current = bid;
        }
        else
        {
            int bpid = girls[gid].current; // 获取女孩当前的舞伴
            // 女孩喜欢bid胜过其当前舞伴的bpid
            if ( GetPerfectPosition(&girls[gid], bpid) > GetPerfectPosition(&girls[gid], bid))
            {
                boys[bpid].current = -1;
                boys[bid].current = gid;
            	girls[gid].current = bid;
            }
        }
        boys[bid].next++;
        bid = FindFreePartner( boys, count );         
    }
    return IsALlPartnerPatch(boys, count);
}
```

## 3. 改进优化

在上述给出的算法的时间复杂度是$O(n^2)$，但还存在一个小小的隐患，那就是GetPerfectPosition（）函数的策略，该函数需要遍历partner的偏爱舞伴列表，很可能导致时间复杂度提高一个数量级。故，需要进行改进，常用的就是以空间换时间。

对于一些在算法执行过程中不会发生变化的静态数据，如果算法执行过程中需要反复读取这些数据，并且读取操作存在一定时间开销的场合。这种情况下比较适合用这种策略。虽然需要一些额外的开销，但相对于$n^2$次查询节省的时间来说，这点开销是能容忍的。

要注意的是，需要设计合理的方式来组织数据。可以用线性表、哈希表等。在本例中，用二维表来表示m在w的偏爱列表中的位置。

```c++
for (int w = 0; w < UNIT_COUNT; w++)
{
    // 初始化成最大值
    for( int j = 0; j < UNIT_COUNT; j++ )
    {
        priority[w][j] = 0x7FFFFFFF;
    }
    // 给偏爱舞伴指定位置关系
    int pos = 0;
    for( int m = 0; m < girls[w].pCount; m++ )
    {
        priority[w][girls[w].perfect[m]] = pos++;
    }
}
```

