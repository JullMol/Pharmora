import csv
import os
from datetime import datetime

FAVORITES_FILE = 'data/user_favorites.csv'
MEDICINE_FILE = 'data/Medicine_Details.csv'  

def add_to_favorites(medicine_name: str):
    medicine_name = medicine_name.strip().lower()
    if not medicine_name:
        print("Nama obat tidak boleh kosong.")
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
        print("File dataset obat tidak ditemukan.")
        return

    if not found:
        print("Obat tidak ditemukan dalam daftar.")
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
        print(f"'{medicine_name}' sudah ada dalam daftar favorit.")
        return

    with open(FAVORITES_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if os.path.getsize(FAVORITES_FILE) == 0:
            writer.writerow(["medicine_name", "timestamp"])
        writer.writerow([medicine_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        print(f"Obat '{medicine_name}' berhasil ditambahkan ke favorit.")


def view_favorites():
    if not os.path.exists(FAVORITES_FILE):
        print("Belum ada obat favorit yang disimpan.")
        return

    with open(FAVORITES_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)
        favorites = list(reader)

        if not favorites:
            print("Belum ada obat favorit yang disimpan.")
            return

        print("\nDaftar Obat Favorit:")
        for idx, (medicine, timestamp) in enumerate(favorites, 1):
            print(f"{idx}. {medicine} (ditambahkan pada {timestamp})")


def remove_from_favorites(medicine_name):
    if not os.path.exists(FAVORITES_FILE):
        print("Tidak ada file favorit untuk dihapus.")
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
        print(f"Obat '{medicine_name}' tidak ditemukan dalam daftar favorit.")
        return

    with open(FAVORITES_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["medicine_name", "timestamp"])
        writer.writerows(updated_rows)

    print(f"Obat '{medicine_name}' berhasil dihapus dari favorit.")