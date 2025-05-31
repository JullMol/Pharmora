import csv
import os
import datetime

class HistoryManager:
    def __init__(self, csv_path="data/search_history.csv"):
        self.csv_path = csv_path
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

    def add_history(self, user_id, search_term):
        with open(self.csv_path, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([user_id, search_term, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    def get_history(self, user_id):
        history = []
        if not os.path.exists(self.csv_path):
            return history
        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3 and str(row[0]) == str(user_id):
                    history.append({
                        "search_term": row[1],
                        "timestamp": row[2]
                    })
        return list(reversed(history))