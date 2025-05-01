class FeedbackNode:
    def __init__(self, medicine_name, rating, comment, timestamp):
        self.medicine_name = medicine_name
        self.rating = rating
        self.comment = comment
        self.timestamp = timestamp
        self.prev = None
        self.next = None

class FeedbackDoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def add_feedback(self, medicine_name, rating, comment, timestamp):
        new_node = FeedbackNode(medicine_name, rating, comment, timestamp)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
    
    def get_all_feedbacks(self):
        feedbacks = []
        current = self.head
        while current:
            feedbacks.append({
                'medicine_name': current.medicine_name,
                'rating': current.rating,
                'comment': current.comment,
                'timestamp': current.timestamp
            })
            current = current.next
        return feedbacks

# ======================================
#        Algoritma: Binary Search
# ======================================

def binary_search(sorted_list, target):
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid].lower() == target.lower():
            return mid
        elif sorted_list[mid].lower() < target.lower():
            low = mid + 1
        else:
            high = mid - 1

    return -1

# ======================================
#          Fungsi Utama: Submit Feedback
# ======================================

import pandas as pd
import datetime

def submit_feedback():
    # Load dataset
    try:
        medicine_df = pd.read_csv('data/Medicine_Details.csv')
    except FileNotFoundError:
        print("Dataset tidak ditemukan.")
        return
    
    if 'Medicine Name' not in medicine_df.columns:
        print("Kolom 'Medicine Names' tidak ditemukan di dataset.")
        return

    medicine_names = sorted(medicine_df['Medicine Name'].tolist())
    feedback_list = FeedbackDoubleLinkedList()

    while True:
        medicine_name = input("\nMasukkan nama obat (atau ketik 'exit' untuk keluar): ").strip()
        if medicine_name.lower() == 'exit':
            break

        index = binary_search(medicine_names, medicine_name)
        if index == -1:
            print("Obat tidak ditemukan. Silakan coba lagi.")
            continue

        print("\nPilih rating:\n1. Excellent\n2. Average\n3. Poor")
        rating_choice = input("Masukkan pilihan rating (1/2/3): ").strip()

        if rating_choice == '1':
            rating_col = 'excellent review'
        elif rating_choice == '2':
            rating_col = 'average review'
        elif rating_choice == '3':
            rating_col = 'poor review'
        else:
            print("Pilihan tidak valid. Ulangi input.")
            continue

        real_index = medicine_df[medicine_df['Medicine Name'].str.lower() == medicine_name.lower()].index[0]
        
        if rating_col in medicine_df.columns:
            medicine_df.at[real_index, rating_col] += 1
        else:
            medicine_df[rating_col] = 0
            medicine_df.at[real_index, rating_col] += 1

        comment = input("Tulis ulasan Anda: ").strip()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        feedback_list.add_feedback(medicine_name, rating_col, comment, timestamp)

        print("✅ Feedback berhasil ditambahkan!")

    medicine_df.to_csv('data/Medicine_Details.csv', index=False)

    feedbacks = feedback_list.get_all_feedbacks()

    if feedbacks:
        try:
            existing_feedbacks = pd.read_csv('data/user_feedbacks.csv')
            new_feedbacks = pd.DataFrame(feedbacks)
            combined = pd.concat([existing_feedbacks, new_feedbacks], ignore_index=True)
            combined.to_csv('data/user_feedbacks.csv', index=False)
        except FileNotFoundError:
            new_feedbacks = pd.DataFrame(feedbacks)
            new_feedbacks.to_csv('data/user_feedbacks.csv', index=False)

    print("\n🚀 Semua feedback berhasil disimpan. Terima kasih!")
