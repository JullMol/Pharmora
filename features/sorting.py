import csv
from models.linked_list import DoubleLinkedList

MEDICINE_FILE = 'data/Medicine_1000_noimage.csv'

def sort_medicines_by_column(column_name, reverse=False):
    try:
        with open(MEDICINE_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)

            if column_name not in reader.fieldnames:
                print(f"Column '{column_name}' not found in the file.")
                return

            medicine_list = DoubleLinkedList()
            for row in data:
                medicine_list.append(row)

            def key_func(item):
                value = item[column_name]
                try:
                    return float(value)
                except ValueError:
                    return value.lower()

            medicine_list.merge_sort(key=key_func)

            sorted_data = medicine_list.to_list()

            if reverse:
                sorted_data = sorted_data[::-1]

            print(f"\nSorting Results Based on: {column_name}")
            for idx, item in enumerate(sorted_data[:10], 1): 
                print(f"{idx}. {item['Medicine Name']} - {item[column_name]}")
    except FileNotFoundError:
        print("Medicine data file not found.")
    except Exception as e:
        print(f"An error occurred during sorting: {e}")