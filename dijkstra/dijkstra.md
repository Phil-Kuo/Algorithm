# Dijkstra 算法

Dijkstra算法是典型的单源最短路径算法。单源可以理解为一个出发点，Dijkstra算法可以求得从这个出发点到图中其他顶点的最短路径，它使用的是广度优先搜索策略。该算法的应用比较广泛，比如地图导航中的道路规划。

## 算法原理

设G = ( V, E )是一个带权有向图，其中s是起点。

Dijkstra算法的思想是用一个辅助数组dist存放当前找到的从s出发到每个顶点的最短路径。dist的初始状态是：dist[$s$] = 0，若存在与s直接相连的顶点$m$，则记录dist[$m$] = $w(s, m)$，其中w就是连接$s$和$m$的边的权值。对于其他与s没有直接相连的顶点$v_i$，则记录dist[$v_i$] = $INF$。Dijkstra算法的基本操作就是利用广度优先搜索策略处理每一个顶点，对与之相关的边进行拓展。

拓展边的方法是：如果存在一条从u到$v_i$的边，那么从s到$v_i$的最短路径可以通过将边$(u, v_i)$添加到尾部来拓展得到，该路径的长度是dist[$u$]+$w(u, v_i)$，在此情况时，进行一个判断：如果这个值比目前已知的dist[$v_i$]的值要小，则执行更新操作dist[$v_i$]$\leftarrow$dist[$u$]+$w(u, v_i)$，否则，不做任何动作。

## 算法实现

Dijkstra算法在搜索过程中需要维护2个顶点集合S、Q，其中集合S存放已知dist[$v_i$]都已经是最短路径的顶点，其余顶点存放于集合Q中。初始集合S为空，每次迭代都从集合Q中选择一个顶点$u$,该顶点满足dist[$u$]最小，然后将该顶点从Q中移到S中。可以看出，起点s总是第一个被选中，这是因为dist[$s$] = 0。

算法的伪代码：

```
algorithm Dijkstra;
begin
    S = {};
    Q = V;
    dist[x] = INF foreach node x in V;
    while Q not empty do
    begin 
    	find node x which satisfy dist[x] = min{D(y): y in Q};
    	S = S.push_back(x);
    	Q = Q.pop(x);
    	UPDATE(x);
    end;
end

Procedure UPDATE(x)
begin
	foreach e(x, y) exist 
		if dist[y] > dist[x]+w(x, y) then 
			dist[y] = dist[x]+w(x, y)
			pred(y) = x;
end
		
```

可利用C++来实现，具体可见「算法的乐趣」第21章。该章详细阐述了针对特定问题的分析，数据结构的确定，进而是算法的实现和演示。