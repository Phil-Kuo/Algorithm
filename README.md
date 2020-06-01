# Algorithm
some codes while learning algorithm

## 利用遗传算法求解函数的最值问题
**gaAlgorithm.py gaIndividual.py objFunction.py:** 基于遗传算法，求解Griewangk function的最小值。定义了算法的选择、交叉、变异操作，并输入函数值-迭代数。**gaAlgorithm.ipynb**实现了与其相似的目的。

## k均值算法

与监督学习不同，非监督学习没有标签变量，需要通过算法模型来挖掘数据内在的结构和模式。主要有两大类方法：**聚类**和**特征变量关联**。

聚类通常是通过多次迭代来找到数据的最优分割。聚类是通过数据之间的内在关系把样本分成若干个类别。K均值聚类（K-Means Clustering）是最基础和常用的聚类算法。

![k_means](C:\Users\Daly Dai\Pictures\k_means.bmp)

#### 1. 基本思想和目标

K均值算法的基本思想是通过迭代方式寻找k个簇，使其聚类结果对应的代价函数最小。一般地，代价函数可以定义为各个样本距离所属簇中心点的**误差平方和**，见下式。该算法的目标是给出给定数据集的划分结果，并给出每个数据对应的簇中心点。
$$
J(c,u) = \sum_{i=1}^M||x_i-u_{c_i}||^2
$$


#### 2. 算法描述
(1) 数据预处理，如归一化、离点群处理；

(2) 随机选取K个簇中心点；

(3)开始迭代，重复以下过程直至代价函数收敛：

- 对于每一个样本，将其分配到距离其最近的簇
  $$
  c_i^{(t)}\leftarrow \underset{k}{\operatorname{argmin}}||x_i-u_k^t||^2
  $$
  
- 对于每一个类簇，重新计算该类簇的中心
  $$
  u_k^{(t+1)}\leftarrow \underset{u}{\operatorname{argmin}}\sum_{i:c_j^{(t)}=k}||x_i-u||^2
  $$
  

详见**k_means_clust.py**，手动实现的k-means算法，性能可能不如sklearn的KMeans。不过对于理解算法的运行有帮助。



#### 3. 调优

(1) 数据归一化和离群点处理。

必不可少。

(2)合理选择K值。

K值的选择一般基于经验和多次实验结果。手肘法（纵轴为误差平方和（或者是定义的其他损失函数），横轴为 K值）法认为拐点就是最佳K值，是一种经验方法。还有一种方法是Gap Statistic方法，只需找到最大Gap statistic对应的K值即可。
$$
Gap（K）=E（log D_k）-log D_k
$$
Gap(K)的物理含义是，随机样本的损失与实际样本的损失之差。

(3)采用核函数。