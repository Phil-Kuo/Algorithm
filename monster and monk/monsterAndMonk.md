# 过河问题

## 1. 问题的提出

问题：有3个传教士（Monk）和3个妖怪（Monster）要利用唯一的一条小船过河，小船的承载上限是2个座位。要求不论是在岸上、船上，传教士的数量均**≥**妖怪的数量，否则传教士就会被妖怪吃掉。待求解的是，构造一个过河的方案，安全地将传教士运送至河对岸。

过河的策略就是无论何时何地都要保证在河的任一侧传教士数量多于妖怪。

## 2. 求解的思路

利用穷举法来求解。使用穷举法的步骤：

> 1. 首先要定义问题的解空间（也叫状态空间，是所有候选解的集合），并分析解空间的拓扑结构。
> 2. 其次再根据解空间进行设计遍历搜索策略。

具体针对实际问题，穷举法的实质就是从初始状态开始，根据某种状态变化规则搜索全部可能的状态，当遇到最终状态后，我们就认为找到了一个解。

### 2.1 定义状态和状态变化的数学模型

如果把任意时刻传教士、妖怪和小船的位置信息看做一个状态，那么要解决的问题就变成了找到从初始状态变换到最终状态的路径。

可以用一个五元组来表示某个时刻的状态：(本地传教士数目、本地妖怪数目、对岸传教士数目、对岸妖怪数目、船的位置)。由此，本问题的初始状态为：**(3,3,0,0，LOCAL)**，最终状态是**（0,0,3,3，REMOTE）**。具体来说，定义状态模型的数据结构为：

```C++
struct ItemState
{
    ...
    int local_monster;
    int local_monk;
    int remote_monster;
    int remote_monk;
    BOAT_LOCATION boat;
};
```

状态变换数学模型使得得到不同的状态，通过穷举各种状态变换动作，找出所有可能的结果，从而使问题得到解决。在本问题中，过河是使得状态发生变换的原因。

可以把过河动作定义为2个内容，即船的位置变化、船上的传教士数目、船上的妖怪数目。具体定义过河动作的数据结构如下：

```c++
typedef struct tagActionEffection
{
	ACTION_NAME actname;
    BOAT_LOCATION boat_to; //船移动的方向
    int move_monster; // 船上的妖怪数目
    int move_monk; // 船上的传教士数目
}ACTION_EFFECTION;
```

其中actname是动作的一个命名。通过对问题的进一步分析，可知，合法的过河动作其实是一个有限的集合。进而得到所有的过河动作列表：

```C++
ACTION_EFFECTION actEffect[] = 
{
	{ ONE_MONSTER_GO ,            REMOTE, -1,  0 },
    { TWO_MONSTER_GO ,            REMOTE, -2,  0 },
    { ONE_MONK_GO ,               REMOTE,  0, -1 },
    { TWO_MONK_GO ,               REMOTE,  0, -2 },
    { ONE_MONSTER_ONE_MONK_GO ,   REMOTE, -1, -1 },
    { ONE_MONSTER_BACK ,          LOCAL ,  1,  0 },
    { TWO_MONSTER_BACK ,          LOCAL ,  2,  0 },
    { ONE_MONK_BACK ,             LOCAL ,  0,  1 },
    { TWO_MONK_BACK ,             LOCAL ,  0,  2 },
    { ONE_MONSTER_ONE_MONK_BACK , LOCAL ,  1,  1 }
}
```

### 2.2 搜索策略

一个状态结合不同的过河动作会迁移到不同的状态。由于过河动作范围仅限于以上10种，穷举的搜索策略就比较直观。将当前状态分别与10种过河动作组合，可以得到状态树上这个状态所有可能的新状态，对每个得到的新状态继续应用10种过河动作，得到新状态，如此不断循环，直至出现最终状态，问题得到求解。

#### 2.2.1 状态树的遍历

状态树的遍历暗含了一个状态生成的过程，就是促使状态树上的一个状态向下一个状态转换的驱动过程，也就是上一节提到的过河动作模型。

状态树遍历的关键是处理过河动作列表actEffect，依次处理一遍该列表中的每个动作，就实现了状态树的遍历。

```c++
for ( int i = 0; i < sizeof( actEffect ) / sizeof( actEffect[0] ); i++)
{
    processStateOnNewAction(states, current, actEffect[i]);
}
```

#### 2.2.2 剪枝和重复状态判断

判断过河动作合法性。不是所有的过河动作都适用于当前状态。

> 1. 首先是当前船的位置决定了某些过河动作的不合理性；
> 2. 其次是移动的传教士或妖怪的数目决定了某些过河动作的不合理性。

应用以上判断，可以省去很多不必要的、甚至是错误的状态变换。

```c++
bool ItemState::CanTakeAction(ACTION_EFFECTION& ae) const
{
    if(boat == ae.boat_to)
        return false;
    if( (local_monster + ae.move_monster) < 0 || (local_monster + ae.move_monster) > monster_count)
        return false;
    if( (local_monk + ae.move_monk) < 0 || (local_monk + ae.move_monk) > monk_count)
        return false;
    return true;
}
```

## 3. 算法的实现

本算法的核心是递归搜索，从初始状态开始调用SearchState()函数。该函数每次从状态队列尾部取出当前要处理的状态，首先判断是否是最终的过河状态（也是递归基），否则尝试用动作列表中的动作与当前状态结合，看看是否能生成合法的新状态。

```c++
/* 能否得到新过河动作 */
bool MakeActionNewState( const ItemState& curState, ACTION_EFFECTION& ae, ItemState& newState)
{
    if ( curState.CanTakeAction(ae) )
    {
        newState = curState;
        newState.local_monster  += ae.move_monster;
        newState.local_monk     += ae.move_monk;
        newState.remote_monster -= ae.move_monster;
        newState.remote_monk    -= ae.move_monk;
        newState.boat    = ae.boat_to;
        newState.curAct  = ae.act;

        return true;
    }

    return false;
}


void SearchState( std::deque<ItemState>& states )
{
    ItemState current = states.back();
    if ( current.IsFinalState() )
    {
        PrintResult(states);
        return;
    }
    /* 尝试用10种动作分别与当前的状态组合 */
    for ( int i = 0; i < sizeof(actEffect) /sizeof(actEffect[0]); i++)
    {
        ItemState next;
        if ( MakeActionNewState(current, actEffect[i], next) )
        {
            if ( next.IsValidState() && !IsProcessedState( states, next ) )
            {
                states.push_back( next );
                SearchState( states );
                states.pop_back();
            }
        }
    }
}
```

