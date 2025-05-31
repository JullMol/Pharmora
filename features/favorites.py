import csv
import os
from datetime import datetime

FAVORITES_FILE = 'data/user_favorites.csv'
MEDICINE_FILE = 'data/Medicine_Details.csv'

def add_to_favorites(user_id, medicine_name: str):
    medicine_name = medicine_name.strip().lower()
    if not medicine_name:
        print("Medicine name cannot be empty.")
        return False

    found_row = None
    try:
        with open(MEDICINE_FILE, mode='r', newline='', encoding='utf-8') as dataset:
            reader = csv.DictReader(dataset)
            for row in reader:
                if row["Medicine Name"].strip().lower() == medicine_name:
                    found_row = row
                    break
    except FileNotFoundError:
        print("Medicine dataset file not found.")
        return False

    if not found_row:
        print("Medicine not found in the list.")
        return False

    favorites = set()
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["user_id"] == str(user_id):
                    favorites.add(row["Medicine Name"].strip().lower())

    if medicine_name in favorites:
        print(f"'{medicine_name}' is already in the favorites list.")
        return False

    with open(FAVORITES_FILE, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ["user_id", "Medicine Name", "Composition", "Uses", "Side_effects", "timestamp"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if os.path.getsize(FAVORITES_FILE) == 0:
            writer.writeheader()
        writer.writerow({
            "user_id": user_id,
            "Medicine Name": found_row.get("Medicine Name", ""),
            "Composition": found_row.get("Composition", ""),
            "Uses": found_row.get("Uses", ""),
            "Side_effects": found_row.get("Side_effects", ""),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        print(f"Medicine '{medicine_name}' has been successfully added to favorites.")
    return True

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

def remove_from_favorites(user_id, medicine_name):
    if not os.path.exists(FAVORITES_FILE):
        return False, "No favorites file found to remove from."

    updated_rows = []
    found = False

    with open(FAVORITES_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not (row["user_id"] == str(user_id) and row["Medicine Name"].strip().lower() == medicine_name.strip().lower()):
                updated_rows.append(row)
            else:
                found = True

    if not found:
        return False, f"Medicine '{medicine_name}' not found in your favorites."

    with open(FAVORITES_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["user_id", "Medicine Name", "Composition", "Uses", "Side_effects", "timestamp"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    return True, f"Medicine '{medicine_name}' has been successfully removed from your favorites."

def get_favorites(user_id):
    if not os.path.exists(FAVORITES_FILE):
        return []

    with open(FAVORITES_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader if row["user_id"] == str(user_id)]