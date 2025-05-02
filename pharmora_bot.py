from models.linked_list import DoubleLinkedList

def chatbot(nodes):
    print("\nPharmora: Hi! I can help you find information about medicines.")
    print("Type 'exit' to quit or 'history' to see your search history.\n")
    
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "keluar"]:
            print("Pharmora: Thank you for using Pharmora. Stay healthy!")
            break
            
        if user_input.lower() in ["history", "riwayat"]:
            print("Pharmora: Search history feature would be implemented here")
            continue

        query = user_input.lower()
        matches = []

        # Search for medicines based on name, uses, or side effects
        for drug in nodes:
            if (drug.uses and query in drug.uses.lower()) or \
               (drug.name and query in drug.name.lower()) or \
               (drug.side_effect and query in drug.side_effect.lower()):
                matches.append(drug)

        if not matches:
            print("Pharmora: I couldn't find medicines related to your query. Could you describe your symptoms or the medicine you're looking for?")
            continue

        reverse = True
        # Use DoubleLinkedList for sorting
        matches_list = DoubleLinkedList()
        for match in matches:
            matches_list.append(match)

        # Sort matches using merge_sort
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
            for i, drug in enumerate(sorted_matches[:5], 1):  # Show top 5 results
                print(f"\n{i}. {drug.name}")
                print(f"   Uses: {drug.uses.split('.')[0] if drug.uses else 'Not specified'}")
                print(f"   Rating: {drug.excellent_review}% positive reviews")
                
        print("\nYou can ask for more details about any of these medicines.")