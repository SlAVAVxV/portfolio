def sum_negatives_between_min_max(arr):
    if not arr:
        return 0
    min_val = min(arr)
    max_val = max(arr)
    min_index = arr.index(min_val)
    max_index = arr.index(max_val)
    start_index = min(min_index, max_index) + 1
    end_index = max(min_index, max_index)
    negative_sum = 0
    for i in range(start_index, end_index):
        if arr[i] < 0:
            negative_sum += arr[i]
    return negative_sum

# Пример использования
A = [3, -1, 2, -4, 5, -6, 1]
result = sum_negatives_between_min_max(A)
print("Сумма отрицательных элементов:", result)