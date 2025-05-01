import csv
from models.medicine import Medicine
from models.linked_list import DoubleLinkedList
from models.search import binary_search
from features.favorites import add_to_favorites, view_favorites, remove_from_favorites
from features.user_feedback import submit_feedback
from features.sorting import sort_medicines_by_column


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


def show_menu():
    print("\n=== MENU PHARMORA ===")
    print("1. Tambah Obat ke Favorit")
    print("2. Lihat Daftar Favorit")
    print("3. Hapus Obat dari Favorit")
    print("4. Kirim Feedback")
    print("5. Sorting Obat Berdasarkan Kolom")
    print("6. Tampilkan Semua Obat")
    print("7. Cari Obat")
    print("0. Keluar")


def main():
    medicine_list = load_medicines('data/Medicine_Details.csv')

    while True:
        show_menu()
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            nama_obat = input("Masukkan nama obat yang ingin ditambahkan ke favorit: ")
            add_to_favorites(nama_obat)

        elif pilihan == "2":
            view_favorites()

        elif pilihan == "3":
            nama_obat = input("Masukkan nama obat yang ingin dihapus dari favorit: ")
            remove_from_favorites(nama_obat)

        elif pilihan == "4":
            print("\n--- Kirim Feedback Pengguna ---")
            submit_feedback()

        elif pilihan == "5":
            print("\nContoh kolom yang bisa digunakan untuk sorting:")
            print("- Medicine Name")
            print("- Manufacturer")
            print("- Excellent Review %")
            print("- Poor Review %")
            print("- Average Review %")
            kolom = input("Masukkan nama kolom yang ingin digunakan untuk sorting: ")
            urutan = input("Urutkan dari terbesar ke terkecil? (y/n): ").lower() == 'y'
            sort_medicines_by_column(kolom, reverse=urutan)

        elif pilihan == "6":
            print("\n--- Daftar Semua Obat ---")
            medicine_list.merge_sort(key=lambda med: med.name.lower())
            medicine_list.display()

        elif pilihan == "7":
            query = input("\nMasukkan nama obat yang ingin dicari: ").strip().lower()
            medicine_list.merge_sort(key=lambda med: med.name.lower())
            sorted_list = medicine_list.to_list()
            result = binary_search(sorted_list, query, key=lambda m: m.name.lower())

            if result:
                print("\nObat ditemukan:")
                print(f"- {result.name} ({result.manufacturer})")
            else:
                print("\nObat tidak ditemukan.")

        elif pilihan == "0":
            print("Terima kasih telah menggunakan Pharmora.")
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    main()