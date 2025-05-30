import csv
import os
from datetime import datetime
import customtkinter as ctk
from models.linked_list import DoubleLinkedList

HISTORY_FILE = 'data/bot_history.csv'

def save_to_csv(user_id, query):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([user_id, query, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def load_from_csv(user_id):
    if not os.path.exists(HISTORY_FILE):
        return []
    history = []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 3 and str(row[0]) == str(user_id):
                history.append(f"{row[1]} ({row[2]})")
    return history

# def chatbot(nodes):
#     print("\nPharmora: Hi! I can help you find information about medicines.")
#     print("Type 'exit' to quit or 'history' to see your search history.\n")

#     search_history = load_from_csv()

#     while True:
#         user_input = input("You: ").strip()
#         if not user_input:
#             continue

#         if user_input.lower() in ["exit", "quit", "keluar"]:
#             print("Pharmora: Thank you for using Pharmora. Stay healthy!")
#             break
            
#         if user_input.lower() in ["history", "riwayat"]:
#             if not search_history:
#                 print("\nPharmora: Your search history is empty.")
#             else:
#                 print("\nPharmora: Here is your search history:")
#                 for i, query in enumerate(search_history, 1):
#                     print(f"{i}. {query}")
#             continue

#         query = user_input.lower()
#         search_history.append(query)
#         save_to_csv(query)
#         matches = []

#         for drug in nodes:
#             if (drug.uses and query in drug.uses.lower()) or \
#                (drug.name and query in drug.name.lower()) or \
#                (drug.side_effect and query in drug.side_effect.lower()):
#                 matches.append(drug)

#         if not matches:
#             print("Pharmora: I couldn't find medicines related to your query. Could you describe your symptoms or the medicine you're looking for?")
#             continue

#         reverse = True
#         matches_list = DoubleLinkedList()
#         for match in matches:
#             matches_list.append(match)

#         matches_list.merge_sort(key=lambda d: d.excellent_review)
#         sorted_matches = matches_list.to_list()
#         if reverse:
#             sorted_matches.reverse()

#         if len(sorted_matches) == 1:
#             drug = sorted_matches[0]
#             print(f"\nPharmora: Based on your query, I found this medicine:")
#             print(f"• {drug.name}")
#             print(f"• Primary Uses: {drug.uses.split('.')[0] if drug.uses else 'Not specified'}")
#             print(f"• Excellent Reviews: {drug.excellent_review}% of users")
#         else:
#             print(f"\nPharmora: I found {len(sorted_matches)} medicines that might help:")
#             for i, drug in enumerate(sorted_matches[:5], 1):
#                 print(f"\n{i}. {drug.name}")
#                 print(f"   Uses: {drug.uses.split('.')[0] if drug.uses else 'Not specified'}")
#                 print(f"   Rating: {drug.excellent_review}% positive reviews")
                
#         print("\nYou can ask for more details about any of these medicines.")

def response_bot(user_input, nodes):
    if user_input.lower() in ["exit", "quit", "keluar"]:
        return "Pharmora: Thank you for using Pharmora. Stay healthy!"

    query = user_input.lower()
    matches = []

    for drug in nodes:
        if (drug.uses and query in drug.uses.lower()) or \
            (drug.name and query in drug.name.lower()) or \
            (drug.side_effect and query in drug.side_effect.lower()):
            matches.append(drug)

    if not matches:
        return "Pharmora: I couldn't find medicines related to your query. Could you describe your symptoms or the medicine you're looking for?\n"

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
        return f"\nPharmora: Based on your query, I found this medicine:\n • {drug.name}\n• Primary Uses: {drug.uses.split('.')[0] if drug.uses else 'Not specified'}\n• Excellent Reviews: {drug.excellent_review}% of users\nYou can ask for more details about this medicine.\n"
    else:
        return f"\nPharmora: I found {len(sorted_matches)} medicines that might help:" + "".join(
            f"\n\n{i+1}. {drug.name}"
            f"\n   Uses: {drug.uses.split('.')[0] if drug.uses else 'Not specified'}"
            f"\n   Rating: {drug.excellent_review}% positive reviews"
            for i, drug in enumerate(sorted_matches[:5])
        ) + "\nYou can ask for more details about any of these medicines.\n"