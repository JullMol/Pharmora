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

    user_id = generate_user_id(username, password)
    hashed_password = hash_password(password)

    with open(USER_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, username, hashed_password, role])
    print(f"User {username} registered successfully with role {role}.")

def login_user(username: str, password: str):
    hashed_password = hash_password(password)
    try:
        with open(USER_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == hashed_password:
                    return row['user_id'], row['role']
    except FileNotFoundError:
        print("Error: Users file not found.")
    return None, None