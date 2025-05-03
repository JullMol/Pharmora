import csv
from models.linked_list import DoubleLinkedList

HISTORY_FILE = 'data/bot_history.csv'

def save_to_csv(query):
    with open(HISTORY_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([query])

def load_from_csv():
    try:
        with open(HISTORY_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader]
    except FileNotFoundError:
        return []

def chatbot(nodes):
    print("\nPharmora: Hi! I can help you find information about medicines.")
    print("Type 'exit' to quit or 'history' to see your search history.\n")

    search_history = load_from_csv()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "keluar"]:
            print("Pharmora: Thank you for using Pharmora. Stay healthy!")
            break
            
        if user_input.lower() in ["history", "riwayat"]:
            if not search_history:
                print("\nPharmora: Your search history is empty.")
            else:
                print("\nPharmora: Here is your search history:")
                for i, query in enumerate(search_history, 1):
                    print(f"{i}. {query}")
            continue

        query = user_input.lower()
        search_history.append(query)
        save_to_csv(query)
        matches = []

        for drug in nodes:
            if (drug.uses and query in drug.uses.lower()) or \
               (drug.name and query in drug.name.lower()) or \
               (drug.side_effect and query in drug.side_effect.lower()):
                matches.append(drug)

        if not matches:
            print("Pharmora: I couldn't find medicines related to your query. Could you describe your symptoms or the medicine you're looking for?")
            continue

        reverse = True
        matches_list = DoubleLinkedList()
        for match in matches:
            matches_list.append(match)

        matches_list.merge_sort(key=lambda d: d.excellent_review)
        sorted_matches = matches_list.to_list()
        if reverse:
            sorted_matches.reverse()

        if len(sorted_matches) == 1:
            drug = sorted_matches[0]
            print(f"\nPharmora: Based on your query, I found this medicine:")
            print(f"• {drug.name}")
            print(f"• Primary Uses: {drug.uses.split('.')[0] if drug.uses else 'Not specified'}")
            print(f"• Excellent Reviews: {drug.excellent_review}% of users")
        else:
            print(f"\nPharmora: I found {len(sorted_matches)} medicines that might help:")
            for i, drug in enumerate(sorted_matches[:5], 1):
                print(f"\n{i}. {drug.name}")
                print(f"   Uses: {drug.uses.split('.')[0] if drug.uses else 'Not specified'}")
                print(f"   Rating: {drug.excellent_review}% positive reviews")
                
        print("\nYou can ask for more details about any of these medicines.")