from models.linked_list import DoubleLinkedList

def chatbot(nodes):
    print("\n=== Pharmora Chatbot 🤖 ===")
    print("Hi! I can help you find information about medicines.")
    print("Examples:")
    print("- Type your disease like: ALzheimer, Migrain, etc.")
    print("- What is Paracetamol?")
    print("- Side effects of Amoxicillin")
    print("- Uses of Ibuprofen")
    print("Type 'exit' to quit or 'history' to see your search history.\n")

    search_history = []

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("\nPharmora: Thank you for using Pharmora Chatbot. Stay healthy!")
            break

        if user_input.lower() in ["history", "riwayat"]:
            if not search_history:
                print("\nPharmora: Your search history is empty.")
            else:
                print("\nPharmora: Here is your search history:")
                for i, query in enumerate(search_history, 1):
                    print(f"{i}. {query}")
            continue

        search_history.append(user_input)

        query = user_input.lower().strip()
        matches = []

        for drug in nodes:
            if (drug.uses and query in drug.uses.lower()) or \
               (drug.name and query in drug.name.lower()) or \
               (drug.side_effect and query in drug.side_effect.lower()):
                matches.append(drug)

        found = False
        for med in nodes:
            name = med.name.lower().strip()

            if name in query:
                if "what is" in query or "information" in query:
                    print(f"\nPharmora:\nName: {med.name}\nUses: {med.uses}\nComposition: {med.composition}")
                elif "side effects" in query:
                    print(f"\nPharmora:\nSide effects of {med.name}: {med.side_effect}")
                elif "uses" in query or "used for" in query:
                    print(f"\nPharmora:\n{med.name} is used for: {med.uses}")
                else:
                    print(f"\nPharmora: Sorry, I don't understand your question about {med.name}.")
                found = True
                break

        if found:
            continue

        if not matches:
            print("\nPharmora: I couldn't find medicines related to your query. Could you describe your symptoms or the medicine you're looking for?")
            continue

        matches_list = DoubleLinkedList()
        for match in matches:
            matches_list.append(match)

        reverse = True

        matches_list.merge_sort(key=lambda d: d.excellent_review)
        sorted_matches = matches_list.to_list()

        if reverse:
            sorted_matches = sorted_matches[::-1]

        if len(sorted_matches) == 1:
            drug = sorted_matches[0]
            print(f"\nPharmora: Based on your query, I found this medicine:")
            print(f"• Name: {drug.name}")
            print(f"• Primary Uses: {drug.uses.split('.')[0] if drug.uses else 'Not specified'}")
            print(f"• Excellent Reviews: {drug.excellent_review}% of users")
            print(f"• Side Effects: {drug.side_effect if drug.side_effect else 'Not specified'}")
        else:
            print(f"\nPharmora: I found {len(sorted_matches)} medicines that might help:")
            for i, drug in enumerate(sorted_matches[:5], 1):
                print(f"\n{i}. {drug.name}")
                print(f"   Uses: {drug.uses.split('.')[0] if drug.uses else 'Not specified'}")
                print(f"   Rating: {drug.excellent_review}% positive reviews")

        print("\nYou can ask for more details about any of these medicines.")