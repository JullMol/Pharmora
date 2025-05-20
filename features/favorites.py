import csv
import os
from datetime import datetime

FAVORITES_FILE = 'data/user_favorites.csv'
MEDICINE_FILE = 'data/Medicine_Details.csv'

def add_to_favorites(medicine_name: str):
    medicine_name = medicine_name.strip().lower()
    if not medicine_name:
        print("Medicine name cannot be empty.")
        return

    found = False
    try:
        with open(MEDICINE_FILE, mode='r', newline='', encoding='utf-8') as dataset:
            reader = csv.DictReader(dataset)
            for row in reader:
                if row["Medicine Name"].strip().lower() == medicine_name:
                    found = True
                    break
    except FileNotFoundError:
        print("Medicine dataset file not found.")
        return

    if not found:
        print("Medicine not found in the list.")
        return

    favorites = set()
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row:
                    favorites.add(row[0].strip().lower())

    if medicine_name in favorites:
        print(f"'{medicine_name}' is already in the favorites list.")
        return

    with open(FAVORITES_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if os.path.getsize(FAVORITES_FILE) == 0:
            writer.writerow(["medicine_name", "timestamp"])
        writer.writerow([medicine_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        print(f"Medicine '{medicine_name}' has been successfully added to favorites.")


def view_favorites():
    if not os.path.exists(FAVORITES_FILE):
        print("No favorite medicines have been saved yet.")
        return

    with open(FAVORITES_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        favorites = list(reader)

        if not favorites:
            print("No favorite medicines have been saved yet.")
            return

        print("\nFavorite Medicines List:")
        for idx, (medicine, timestamp) in enumerate(favorites, 1):
            print(f"{idx}. {medicine} (added on {timestamp})")


def remove_from_favorites(medicine_name):
    if not os.path.exists(FAVORITES_FILE):
        print("No favorites file found to remove from.")
        return

    updated_rows = []
    found = False

    with open(FAVORITES_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        for row in reader:
            if row and row[0].strip().lower() != medicine_name.lower():
                updated_rows.append(row)
            else:
                found = True

    if not found:
        print(f"Medicine '{medicine_name}' not found in the favorites list.")
        return

    with open(FAVORITES_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["medicine_name", "timestamp"])
        writer.writerows(updated_rows)

    print(f"Medicine '{medicine_name}' has been successfully removed from favorites.")

def get_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return []

    with open(FAVORITES_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        return [(row[0], row[1]) for row in reader if row]