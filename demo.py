# 打印100以内的偶数
#
# for i in range(0, 101, 2):
#     print(i, end=" ")

# 二分叉查找
#
def binary_search(li, val):
    left = 0
    right = len(li) - 1
    while left <= right:
        mid = (left + right) // 2
        if li[mid] == val:
            return mid
        elif li[mid] > val:
            right = mid - 1
        else:
            left = mid + 1
    return -1


li = [1, 3, 5, 7, 9]
print(binary_search(li, 3))
print(binary_search(li, 10))
print(binary_search(li, 1))
print(binary_search(li, 9))
print(binary_search(li, 5))
print(binary_search(li, 7))
print(binary_search(li, 2))
print(binary_search(li, 4))
print(binary_search(li, 6))
print(binary_search(li, 8))
print(binary_search(li, 0))

