from models.medicine import Medicine

class Node:
    def __init__(self, data: Medicine):
        self.data = data
        self.prev = None
        self.next = None

class DoubleLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data: Medicine):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last
    
    def display(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def merge_sort(self, key=lambda med: med.name.lower()):
        def merge_sort_iterative(head, key):
            if not head or not head.next:
                return head

            def get_length(head):
                length = 0
                current = head
                while current:
                    length += 1
                    current = current.next
                return length

            def split(head, step):
                current = head
                prev = None
                for _ in range(step):
                    if not current:
                        break
                    prev = current
                    current = current.next
                if prev:
                    prev.next = None
                return head, current

            def merge(left, right):
                dummy = Node(None)
                current = dummy
                while left and right:
                    if key(left.data) <= key(right.data):
                        current.next = left
                        left.prev = current
                        left = left.next
                    else:
                        current.next = right
                        right.prev = current
                        right = right.next
                    current = current.next
                if left:
                    current.next = left
                    left.prev = current
                if right:
                    current.next = right
                    right.prev = current
                return dummy.next

            length = get_length(head)
            dummy = Node(None)
            dummy.next = head
            step = 1

            while step < length:
                current = dummy.next
                tail = dummy

                while current:
                    left = current
                    right = split(left, step)[1]
                    current = split(right, step)[1]
                    merged = merge(left, right)
                    tail.next = merged

                    while tail.next:
                        tail = tail.next

                step *= 2

            return dummy.next

        self.head = merge_sort_iterative(self.head, key)