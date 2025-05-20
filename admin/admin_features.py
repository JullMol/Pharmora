import csv
import os

CSV_FILE = 'C:/Users/LENOVO/OneDrive/Documents/Semester 2/Struktur Data dan Algoritma/Pharmora/data/Medicine_1000_noimage.csv'

def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Composition', 'Uses', 'Side Effects'])

def add_medicine(name, composition, uses, side_effect):
    ensure_csv_exists()
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].lower() == name.lower():
                return False, "Medicine already exists."

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, composition, uses, side_effect])
    return True, f"Medicine {name} added successfully."

def view_medicine_data():
    ensure_csv_exists()
    data = []
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) >= 4:
                data.append(row[:4])
    return data

def delete_medicine(name):
    ensure_csv_exists()
    temp_file = 'data/temp_Medicine_1000_cleaned.csv'
    found = False

    with open(CSV_FILE, mode='r', encoding='utf-8') as file, \
         open(temp_file, mode='w', newline='', encoding='utf-8') as temp:
        reader = csv.reader(file)
        writer = csv.writer(temp)

        for row in reader:
            if row[0].lower() == name.lower():
                found = True
                continue
            writer.writerow(row)

    if found:
        os.replace(temp_file, CSV_FILE)
        return True, f"Medicine {name} deleted successfully."
    else:
        os.remove(temp_file)
        return False, f"Medicine {name} not found."