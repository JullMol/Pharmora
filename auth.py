# import csv
# import hashlib
# import os

# USER_FILE = 'data/users.csv'

# def hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()

# def generate_user_id(username, password):
#     return str(hash(username + str(password)))

# def is_username_exist(username: str) -> bool:
#     if not os.path.exists(USER_FILE):
#         return False
#     with open(USER_FILE, mode='r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             if row['username'] == username:
#                 return True
#     return False

# def register_user(username: str, password: str, role: str):
#     if not os.path.exists(USER_FILE):
#         with open(USER_FILE, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(['user_id', 'username', 'password', 'role'])

#     user_id = generate_user_id(username, password)
#     hashed_password = hash_password(password)

#     with open(USER_FILE, mode='a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow([user_id, username, hashed_password, role])
#     print(f"User {username} registered successfully with role {role}.")

# def login_user(username: str, password: str, expected_role: str):
#     hashed_password = hash_password(password)
#     try:
#         with open(USER_FILE, mode='r', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 if row['username'] == username and row['password'] == hashed_password:
#                     if row['role'] == expected_role:
#                         return row['user_id'], row['role']
#                     else:
#                         return None, "wrong_role"
#     except FileNotFoundError:
#         print("Error: Users file not found.")
#     return None, None


import csv
import hashlib
import os

USER_FILE = 'data/users.csv'

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_user_id(username, password):
    return str(hash(username + str(password)))

def register_user(username: str, password: str, role: str):
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'username', 'password', 'role'])

    if is_username_exist(username):
        print("Registration Failed: Username already exists.")
        return False

    user_id = generate_user_id(username, password)
    hashed_password = hash_password(password)

    with open(USER_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, username, hashed_password, role])
    
    print(f"User {username} registered successfully with role {role}.")
    return True

def login_user(username: str, password: str):
    hashed_password = hash_password(password)
    try:
        with open(USER_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == hashed_password:
                    if row['role'] == "admin":
                        return row['user_id'], row['role']
                    if row['role'] == "user":
                        return row['user_id'], row['role']
                    else:
                        print("Access Denied: Not an admin.")
                        return None, None
    except FileNotFoundError:
        print("Error: Users file not found.")
    return None, None

def is_username_exist(username: str) -> bool:
    if not os.path.exists(USER_FILE):
        return False
    
    with open(USER_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                return True
    return False
