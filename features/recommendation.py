from loader import load_medicines
from models.search import binary_search
from difflib import get_close_matches

CSV_PATH = 'data/Medicine_1000_noimage.csv'

def find_similar_by_name(drug_name, all_names, all_nodes):
    matches = get_close_matches(drug_name, all_names, n=3, cutoff=0.6)
    results = []
    for match in matches:
        idx = all_names.index(match)
        results.append(all_nodes[idx])
    return results

def find_by_keyword(keyword, head):
    keyword_lower = keyword.lower()
    results = []
    current = head
    while current:
        if (
            current.data.uses and keyword_lower in current.data.uses.lower()
        ) or (
            current.data.side_effect and keyword_lower in current.data.side_effect.lower()
        ):
            results.append(current.data)
        current = current.next
    return results

def drug_search_main():
    drug_list = load_medicines(CSV_PATH)
    drug_list.merge_sort(key=lambda med: med.name.lower())
    nodes = drug_list.to_list()
    all_names = [node.name.lower() for node in nodes]

    while True:
        query = input("\nEnter drug name or keyword (or 'back' to exit): ").strip().lower()
        if query == 'back':
            break

        matched_name = binary_search(all_names, query, key=lambda x: x.lower())
        if matched_name:
            selected = None
            for drug in nodes:
                if drug.name.lower() == matched_name:
                    selected = drug
                    break

            if selected:
                print(f"\nName: {selected.name}")
                print(f"Uses: {selected.uses}")
                print(f"Side Effects: {selected.side_effect}")

                print("\nSimilar recommendations:")
                similar = find_by_keyword(selected.uses, drug_list.head)
                for sim in similar:
                    if sim.name.lower() != selected.name.lower():
                        print(f"- {sim.name} (Uses: {sim.uses})")
            else:
                print("Obat ditemukan, tetapi gagal mengambil detail obat.")
        else:
            results = find_by_keyword(query, drug_list.head)
            if results:
                print("\nDrugs found by keyword:")
                for drg in results:
                    print(f"- {drg.name} (Uses: {drg.uses})")
            else:
                print("No matching medicine found.")
