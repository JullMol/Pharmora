import csv
from models.medicine import Medicine
from models.linked_list import DoubleLinkedList

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
                manufacturer=row['Manufacturer'],
                excellent_review=row['Excellent Review %'],
                average_review=row['Average Review %'],
                poor_review=row['Poor Review %']
            )
            dll.append(med)
            med_id_counter += 1
    return dll