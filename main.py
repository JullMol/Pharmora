import csv
from models.medicine import Medicine
from models.linked_list import DoubleLinkedList
from models.search import binary_search

def load_medicines(file_path):
    dll = DoubleLinkedList()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        med_id_counter = 1
        for row in reader:
            med = Medicine(
                med_id=f"MED{med_id_counter:03}",
                name=row['Medicine Name'],
                composition=row['Composition'],
                uses=row['Uses'],
                side_effect=row['Side_effects'],
                image_url=row['Image URL'],
                manufacturer=row['Manufacturer'],
                excellent_review=row['Excellent Review %'],
                average_review=row['Average Review %'],
                poor_review=row['Poor Review %']
            )
            dll.append(med)
            med_id_counter += 1
    return dll

if __name__ == "__main__":
    medicine_list = load_medicines('data/Medicine_Details.csv')
    print(f"Before Sorting: ")
    medicine_list.display()


    medicine_list.merge_sort(key=lambda m: m.name.lower())
    print(f"\nAfter Sorting: ")
    medicine_list.display()

    sorted_list = medicine_list.to_list()
    query = input("\nEnter the name of the medicine to search for: ")
    result = binary_search(sorted_list, query, key=lambda m: m.name.lower())

    if result:
        print(f"\nMedicines found: {result}")
    else:
        print("\nMedicines not found.")