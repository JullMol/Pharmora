def binary_search(data, target, key=lambda x: x):
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_value = key(data[mid])
        if mid_value == target:
            return data[mid]
        elif mid_value < target:
            low = mid + 1
        else:
            high = mid - 1
    return None