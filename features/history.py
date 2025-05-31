import os

HISTORY_PATH = 'data/History.csv'

def save_search_to_history(query, history_path=HISTORY_PATH):
    with open(history_path, 'a', encoding='utf-8') as f:
        f.write(query + '\n')

def show_search_history(history_path=HISTORY_PATH):
    if not os.path.exists(history_path):
        print("No search history found.")
        return
    with open(history_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            print("\n--- Search History (Last 10) ---")
            for line in lines[-10:]:
                print("- " + line.strip())
        else:
            print("Search history is empty.")