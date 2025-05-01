import csv

MEDICINE_FILE = 'data/Medicine_Details.csv'

def merge_sort(data, key_func, reverse=False):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid], key_func, reverse)
    right = merge_sort(data[mid:], key_func, reverse)

    return merge(left, right, key_func, reverse)

def merge(left, right, key_func, reverse):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if reverse:
            if key_func(left[i]) > key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            if key_func(left[i]) < key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def sort_medicines_by_column(column_name, reverse=False):
    try:
        with open(MEDICINE_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)

            if column_name not in reader.fieldnames:
                print(f"Column '{column_name}' not found in the file.")
                return

            def key_func(item):
                value = item[column_name]
                try:
                    return float(value)
                except ValueError:
                    return value.lower()

            sorted_data = merge_sort(data, key_func, reverse)

            print(f"\nSorting Results Based on: {column_name}")
            for idx, item in enumerate(sorted_data[:10], 1): 
                print(f"{idx}. {item['Medicine Name']} - {item[column_name]}")
    except FileNotFoundError:
        print("Medicine data file not found.")
    except Exception as e:
        print(f"An error occurred during sorting: {e}")