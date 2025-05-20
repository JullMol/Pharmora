from auth import register_user, login_user
from user.dashboard import user_dashboard, user
from admin.dashboard import admin_dashboard

def main():
    while True:
        print("\n=== PHARMORA MAIN MENU ===")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Register New User")
        print("0. Exit")

        pilihan = input("Choose an option: ")

        if pilihan == "1":
            username = input("Username: ")
            password = input("Password: ")
            user_id, role = login_user(username, password)

            if user_id is None:
                print("Invalid login credentials.")
            elif role == "admin":
                print(f"Welcome, {username}!")
                admin_dashboard()
            else:
                print("Access denied. Admins only.")

        elif pilihan == "2":
            username = input("Username: ")
            password = input("Password: ")
            user_id, role = login_user(username, password, expected_role="user")

            if user_id is None:
                print("Invalid login credentials.")
            elif role == "user":
                print(f"Welcome, {username}!")
                user_dashboard()
                user()
            else:
                print("Access denied. Users only.")

        elif pilihan == "3":
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            role = input("Enter role (admin/user): ").strip().lower()
            if role not in ["admin", "user"]:
                print("Invalid role. Please choose 'admin' or 'user'.")
            else:
                register_user(username, password, role)

        elif pilihan == "0":
            print("Thank you for using Pharmora.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()