from models.item import Item

class Book(Item):
    def __init__(self, item_id, name, base_price, quantity, author):
        super().__init__(item_id, name, base_price, quantity)
        self.author = author  # Thuộc tính riêng: Tác giả
    def tinh_gia_ban(self):
        return self.base_price * 1.05  # Đa hình: Sách tính thêm 5% thuế

class Magazines(Item):
    def __init__(self, item_id, name, base_price, quantity, issue_number):
        super().__init__(item_id, name, base_price, quantity)
        self.issue_number = issue_number  # Thuộc tính riêng: Số phát hành

class Newspapers(Item):
    def __init__(self, item_id, name, base_price, quantity, date):
        super().__init__(item_id, name, base_price, quantity)
        self.date = date  # Thuộc tính riêng: Ngày phát hành

class Theses(Item):
    def __init__(self, item_id, name, base_price, quantity, university):
        super().__init__(item_id, name, base_price, quantity)
        self.university = university  # Thuộc tính riêng: Trường đại học

class Manuscripts(Item):
    def __init__(self, item_id, name, base_price, quantity, century):
        super().__init__(item_id, name, base_price, quantity)
        self.century = century  # Thuộc tính riêng: Thế kỷ