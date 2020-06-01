## 快速排序

快速排序与冒泡排序类似，也是一种交换排序，通过元素之间的比较和交换位置来实现。在平均状况下的时间复杂度是O(nlogn),空间复杂度是O(logn)~O(n),并且快速排序是一种不稳定的排序算法。

### 基本思想：

> 1. 采用分而治之思想
> 2. 确定基准元素，通过比较各元素与基准元素的大小关系，将元素分为两组，将小于基准元素的所有元素移动到左边，将大于的移动到右边，由此将问题分解为两部分。
> 3. 分别对两部分重复第2步直至无法再分。

```
def quick_sort_custom(arr, start, end):
    if start >= end:
        return
    else:
        pivot_index = partion(arr, start, end)
        quick_sort_custom(arr, start, pivot_index-1)
        quick_sort_custom(arr, pivot_index+1, end)

def partion(arr,  start, end):
    pivot = arr[start]
    i = left = start
    right = end
    while i<=right:
        if arr[i]<pivot:
            arr[left], arr[i] = arr[i], arr[left]
            left += 1
            i += 1
        elif arr[i]>pivot:
            arr[right], arr[i] = arr[i],arr[right]
            right -= 1
        else:
            i += 1
    return right

if __name__ =="__main__":
    unsorted = [-3,-4,-6]
    quick_sort_custom(unsorted, 0, len(unsorted)-1)
    print(unsorted)
```