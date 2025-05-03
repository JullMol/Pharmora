import csv
import os

def add_medicine(name, composition, uses, side_effect):
    with open('data/Medicine_Details.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == name:
                print("Medicine already exists.")
                return
    with open('data/Medicine_Details.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, composition, uses, side_effect])
    print(f"Medicine {name} added successfully.")

def view_medicine_data():
    print("\nMedicine Data:")
    with open('data/Medicine_Details.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"Name: {row[0]}, Composition: {row[1]}, Uses: {row[2]}, Side Effects: {row[3]}")

def delete_medicine(name):
    temp_file = 'data/temp_medicine_details.csv'
    found = False

    with open('data/Medicine_Details.csv', mode='r', encoding='utf-8') as file, \
         open(temp_file, mode='w', newline='', encoding='utf-8') as temp:
        reader = csv.reader(file)
        writer = csv.writer(temp)

        for row in reader:
            if row[0].lower() == name.lower():
                found = True
                print(f"Medicine {name} deleted successfully.")
                continue
            writer.writerow(row)

    if found:
        os.replace(temp_file, 'data/Medicine_Details.csv')
    else:
        os.remove(temp_file)
        print(f"Medicine {name} not found.")