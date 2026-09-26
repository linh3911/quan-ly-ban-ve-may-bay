class Item:
    def __init__(self, item_id, name, base_price, quantity):
        # Ép kiểu dữ liệu id thành chuỗi ký tự (str) để luôn so khớp được chuỗi tìm kiếm
        self.id = str(item_id).strip()
        self.name = name
        self.base_price = float(base_price)
        self.quantity = int(quantity)

    def tinh_gia_ban(self):
        """Tính giá bán (Tính đa hình - sẽ được ghi đè ở các lớp con)"""
        return self.base_price

    def __str__(self):
        return f"[{self.id}] {self.name} - Giá: {self.tinh_gia_ban():,.0f}đ - SL: {self.quantity}"