import tkinter as tk
from tkinter import messagebox, ttk

class ItemDialog(tk.Toplevel):
    def __init__(self, parent, title, item_data=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("380x320")
        self.result = None
        self.grab_set()  # Khóa màn hình chính cho đến khi xử lý xong hộp thoại này

        # Tạo các nhãn (Label) và ô nhập liệu (Entry)
        tk.Label(self, text="Mã sản phẩm:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.txt_id = tk.Entry(self)
        self.txt_id.grid(row=0, column=1, padx=10, pady=5)
        if item_data:
            self.txt_id.insert(0, item_data['id'])
            self.txt_id.config(state="disabled")

        tk.Label(self, text="Tên sản phẩm:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txt_name = tk.Entry(self)
        self.txt_name.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Loại mặt hàng:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.cbo_type = ttk.Combobox(self, values=["Book", "Magazines", "Newspapers", "Theses", "Manuscripts"], state="readonly")
        self.cbo_type.grid(row=2, column=1, padx=10, pady=5)
        self.cbo_type.set("Book")

        tk.Label(self, text="Giá gốc cơ bản:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.txt_price = tk.Entry(self)
        self.txt_price.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self, text="Số lượng kho:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.txt_qty = tk.Entry(self)
        self.txt_qty.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self, text="Thuộc tính riêng:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.txt_extra = tk.Entry(self)
        self.txt_extra.grid(row=5, column=1, padx=10, pady=5)

        # Nếu là chế độ Sửa, tự động điền thông tin cũ vào các ô
        if item_data:
            self.txt_name.insert(0, item_data['name'])
            self.cbo_type.set(item_data['type'])
            self.txt_price.insert(0, item_data['base_price'])
            self.txt_qty.insert(0, item_data['quantity'])
            self.txt_extra.insert(0, item_data['extra'])

        # Nút Lưu dữ liệu
        tk.Button(self, text="Lưu thông tin", command=self.on_save, bg="#4CAF50", fg="white").grid(row=6, column=0, columnspan=2, pady=15)

    def on_save(self):
        """Bắt lỗi ngoại lệ và kiểm tra tính hợp lệ dữ liệu nhập vào"""
        try:
            item_id = self.txt_id.get().strip()
            name = self.txt_name.get().strip()
            price = float(self.txt_price.get())
            qty = int(self.txt_qty.get())
            extra = self.txt_extra.get().strip()

            # Kiểm tra lỗi bỏ trống ô hoặc nhập số âm
            if not item_id or not name or not extra:
                raise ValueError("Không được bỏ trống các ô thông tin.")
            if price < 0 or qty < 0:
                raise ValueError("Giá gốc và Số lượng tồn kho không được là số âm.")

            self.result = {
                "id": item_id, "name": name, "type": self.cbo_type.get(),
                "base_price": price, "quantity": qty, "extra": extra
            }
            self.destroy()
        except ValueError as e:
            # Hiển thị hộp thoại cảnh báo lỗi
            messagebox.showerror("Lỗi nhập liệu", f"Dữ liệu sai: {str(e)}")