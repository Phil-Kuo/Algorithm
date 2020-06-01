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
