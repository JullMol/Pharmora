import csv
import datetime
import os

FEEDBACK_FILE = 'data/user_feedbacks.csv'

def add_user_feedback(user_id, username, medicine_name, rating, comment):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fieldnames = ["user_id", "username", "medicine_name", "rating", "comment", "timestamp"]
    write_header = not os.path.exists(FEEDBACK_FILE) or os.path.getsize(FEEDBACK_FILE) == 0
    with open(FEEDBACK_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow({
            "user_id": user_id,
            "username": username,
            "medicine_name": medicine_name,
            "rating": rating,
            "comment": comment,
            "timestamp": timestamp
        })
    return True, "Feedback successfully added!"

def get_feedbacks_by_user(user_id):
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader if row["user_id"] == str(user_id)]

def get_feedbacks_by_medicine(medicine_name):
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader if row["medicine_name"].lower() == medicine_name.lower()]
    
def get_all_feedbacks():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)