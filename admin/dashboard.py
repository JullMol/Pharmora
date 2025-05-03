from admin.admin_features import add_medicine, view_medicine_data, delete_medicine

def admin_dashboard():
    while True:
        print("\n=== ADMIN DASHBOARD ===")
        print("1. Add Medicine")
        print("2. View Medicine Data")
        print("3. Delete Medicine")
        print("0. Logout")

        pilihan = input("Choose an option: ")

        if pilihan == "1":
            name = input("Enter medicine name: ")
            composition = input("Enter composition: ")
            uses = input("Enter uses: ")
            side_effect = input("Enter side effects: ")
            add_medicine(name, composition, uses, side_effect)

        elif pilihan == "2":
            view_medicine_data()

        elif pilihan == "3":
            name = input("Enter the name of the medicine to delete: ")
            delete_medicine(name)

        elif pilihan == "0":
            print("Logging out...")
            break

        else:
            print("Invalid option. Please try again.")