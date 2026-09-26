class Node:
    def __init__(self, data=None):
        self.data = data  # Chứa đối tượng sản phẩm (Book, Magazines,...)
        self.next = None  # Liên kết tới nút tiếp theo
        self.prev = None  # Liên kết tới nút phía trước

class DoublyLinkedList:
    def __init__(self):
        self.head = None  # Nút đầu tiên
        self.tail = None  # Nút cuối cùng

    def insert_tail(self, data):
        """Thêm một sản phẩm mới vào cuối danh sách liên kết đôi"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove_node(self, item_id):
        """Xóa một sản phẩm khỏi danh sách theo Mã số (ID)"""
        curr = self.head
        while curr:
            if curr.data.id == item_id:
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev
                return True
            curr = curr.next
        return False

    def search_by_id(self, item_id):
        """Tìm kiếm sản phẩm chính xác theo Mã số (ID)"""
        curr = self.head
        while curr:
            if curr.data.id == item_id:
                return curr.data
            curr = curr.next
        return None

    def to_list(self):
        """Chuyển đổi tạm thời sang list thường để đổ dữ liệu hiển thị lên giao diện bảng"""
        res = []
        curr = self.head
        while curr:
            res.append(curr.data)
            curr = curr.next
        return res

    def sort_list(self, criteria="id", reverse=False):
        """Thuật toán Merge Sort nâng cao để sắp xếp trực tiếp trên các liên kết con trỏ"""
        if not self.head or not self.head.next:
            return

        def get_val(item):
            if criteria == "name": return item.name.lower()
            if criteria == "price": return item.tinh_gia_ban()
            if criteria == "quantity": return item.quantity
            return item.id

        def split(node):
            fast = slow = node
            while fast.next and fast.next.next:
                fast = fast.next.next
                slow = slow.next
            temp = slow.next
            slow.next = None
            if temp: temp.prev = None
            return temp

        def merge(first, second):
            if not first: return second
            if not second: return first
            
            v1 = get_val(first.data)
            v2 = get_val(second.data)
            condition = v1 <= v2 if not reverse else v1 >= v2
            
            if condition:
                first.next = merge(first.next, second)
                if first.next: first.next.prev = first
                first.prev = None
                return first
            else:
                second.next = merge(first, second.next)
                if second.next: second.next.prev = second
                second.prev = None
                return second

        def merge_sort(node):
            if not node or not node.next: return node
            second = split(node)
            node = merge_sort(node)
            second = merge_sort(second)
            return merge(node, second)

        self.head = merge_sort(self.head)
        curr = self.head
        while curr and curr.next: curr = curr.next
        self.tail = curr