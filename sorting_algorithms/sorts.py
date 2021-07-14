from random import shuffle

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def bubble_sort(arr):
    swapped = False
    for i in range(len(arr) - 1):
        for j in range(1, len(arr) - i):
            if arr[j-1] > arr[j]:
                swapped = True
                swap(arr, j, j-1)
                yield arr, j, (None, ), j-1
            else:
                yield arr, j-1, (None, ), j
        if not swapped:
            break

def selection_sort(arr):
    for i in range(len(arr)-1):
        smallest = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[smallest]:
                smallest = j
            yield arr, smallest, (None, ), j
        swap(arr, i, smallest)

def insertion_sort(arr):
    for i in range(1, len(arr)):
        insert_item = arr[i]
        j = i - 1
        while j >= 0 and insert_item <= arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, i, (None, ), j
        arr[j+1] = insert_item
        yield arr, j + 1, (None, ), i

def merge(arr, low, mid, high):
    merged = []
    l_index = low
    r_index = mid + 1

    while l_index <= mid and r_index <= high:
        if arr[l_index] < arr[r_index]:
            merged.append(arr[l_index])
            l_index += 1
        else:
            merged.append(arr[r_index])
            r_index += 1

    while l_index <= mid:
        merged.append(arr[l_index])
        l_index += 1

    while r_index <= high:
        merged.append(arr[r_index])
        r_index += 1

    for ind, value in enumerate(merged):
        arr[low + ind] = value
        yield arr, high, (mid, ), low + ind

def merge_sort(arr, low, high):
    if low >= high:
        return arr

    mid = low + ((high - low + 1) // 2) - 1

    yield from merge_sort(arr, low, mid)
    yield from merge_sort(arr, mid + 1, high)

    yield from merge(arr, low, mid, high)

def quick_sort(arr, low, high):
    if low >= high:
        return arr

    pivot = arr[high]
    pivot_index = low
    for i in range(low, high):
        if arr[i] < pivot:
            swap(arr, i, pivot_index)
            pivot_index += 1
        yield arr, low, (pivot_index, i), high
    swap(arr, high, pivot_index)
    yield arr, low, (pivot_index, i), high

    yield from quick_sort(arr, low, pivot_index - 1)
    yield from quick_sort(arr, pivot_index + 1, high)

def bogo_sort(arr):
    flag = True
    while flag:
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                yield arr, -1, (None, ), -1
                shuffle(arr)
                break
        else:
            yield sorted(arr), None, (None, ), None
            flag = False