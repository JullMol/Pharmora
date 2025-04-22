def binary_search(data_list, target, key=lambda x: x.name.lower()):
    left = 0
    right = len(data_list) - 1
    target = target.lower()

    while left <= right:
        mid = (left + right) // 2
        mid_value = key(data_list[mid])

        if mid_value == target:
            return data_list[mid]
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return None