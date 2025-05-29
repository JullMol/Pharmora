from models.linked_list import DoubleLinkedList

def binary_search_suggestions(data_list, prefix):
    left = 0
    right = len(data_list) - 1
    suggestions = []

    while left <= right:
        mid = (left + right) // 2
        if data_list[mid].lower().startswith(prefix.lower()):
            i = mid
            while i >= 0 and data_list[i].lower().startswith(prefix.lower()):
                suggestions.append(data_list[i])
                i -= 1
            i = mid + 1
            while i < len(data_list) and data_list[i].lower().startswith(prefix.lower()):
                suggestions.append(data_list[i])
                i += 1
            break
        elif data_list[mid].lower() < prefix.lower():
            left = mid + 1
        else:
            right = mid - 1
    
    dll = DoubleLinkedList()
    for s in suggestions:
        dll.append(s)
    dll.merge_sort(key=lambda x: x.lower())
    return dll.to_list()