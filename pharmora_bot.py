def chatbot(nodes):
    print("\n=== Pharmora Chatbot 🤖 ===")
    print("Ask me about medicines! Examples:")
    print("- What is Paracetamol?")
    print("- Side effects of Amoxicillin")
    print("- Uses of Ibuprofen")
    print("Type 'exit' to leave the chatbot.\n")

    while True:
        user_input = input("You: ").strip().lower()

        if user_input in ["exit", "quit"]:
            print("Chatbot: Thank you! See you next time.")
            break

        found = False
        for med in nodes:
            name = med.name.lower()

            if name in user_input:
                if "what is" in user_input or "information" in user_input:
                    print(f"Chatbot:\nName: {med.name}\nUses: {med.uses}\nComposition: {med.composition}")
                elif "side effects" in user_input:
                    print(f"Chatbot: Side effects of {med.name}: {med.side_effect}")
                elif "uses" in user_input or "used for" in user_input:
                    print(f"Chatbot: {med.name} is used for: {med.uses}")
                else:
                    print(f"Chatbot: Sorry, I don't understand your question about {med.name}.")
                found = True
                break

        if not found:
            print("Chatbot: Sorry, I couldn't find information about the medicine you mentioned.")