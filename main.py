import csv
from loader import load_medicines
from models.search import binary_search
from features.favorites import add_to_favorites, view_favorites, remove_from_favorites
from features.user_feedback import submit_feedback
from features.sorting import sort_medicines_by_column
from features.history import save_search_to_history, show_search_history
from features.recommendation import drug_search_main
from pharmora_bot import chatbot

def show_menu():
    print("\n=== PHARMORA MENU ===")
    print("1. Display All Medicines")
    print("2. Search Medicine")
    print("3. Sort Medicines by Column")
    print("4. Add Medicine to Favorites")
    print("5. View Favorites List")
    print("6. Remove Medicine from Favorites")
    print("7. Medicine Recommendations")
    print("8. View Search History")
    print("9. Submit Feedback")
    print("10. Pharmora Chatbot")
    print("0. Exit")

def main():
    medicine_list = load_medicines('data/Medicine_Details.csv')

    while True:
        show_menu()
        pilihan = input("Choose an option: ")

        if pilihan == "1":
            print("\n--- List of All Medicines ---")
            medicine_list.merge_sort(key=lambda med: med.name.lower())
            medicine_list.display()

        elif pilihan == "2":
            query = input("\nEnter the name of the medicine to search for: ").strip().lower()
            medicine_list.merge_sort(key=lambda med: med.name.lower())
            sorted_list = medicine_list.to_list()
            result = binary_search(sorted_list, query, key=lambda m: m.name.lower())

            if query:
                save_search_to_history(query)

            if result:
                print("\nMedicine found:")
                print(f"- {result.name} ({result.manufacturer})")
            else:
                print("\nMedicine not found.")

        elif pilihan == "3":
            print("\nExamples of columns that can be used for sorting:")
            print("- Medicine Name")
            print("- Manufacturer")
            print("- Excellent Review %")
            print("- Poor Review %")
            print("- Average Review %")
            kolom = input("Enter the column name to use for sorting: ")
            urutan = input("Sort from largest to smallest? (y/n): ").lower() == 'y'
            sort_medicines_by_column(kolom, reverse=urutan)

        elif pilihan == "4":
            nama_obat = input("Enter the name of the medicine to add to favorites: ")
            add_to_favorites(nama_obat)

        elif pilihan == "5":
            view_favorites()

        elif pilihan == "6":
            nama_obat = input("Enter the name of the medicine to remove from favorites: ")
            remove_from_favorites(nama_obat)

        elif pilihan == "7":
            print("\n--- Medicine Recommendations ---")
            drug_search_main()

        elif pilihan == "8":
            print("\n--- Search History ---")
            show_search_history()

        elif pilihan == "9":
            print("\n--- Submit User Feedback ---")
            submit_feedback()

        elif pilihan == "10":
            print("\n--- Pharmora Chatbot ---")
            nodes = medicine_list.to_list()
            chatbot(nodes)

        elif pilihan == "0":
            print("Thank you for using Pharmora.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()