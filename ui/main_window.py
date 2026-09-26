import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from models.linked_list import DoublyLinkedList
from models.subclasses import Book, Magazines, Newspapers, Theses, Manuscripts
from ui.dialogs import ItemDialog

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống Quản lý Cửa hàng Sách")
        self.geometry("900x500")
        self.db_path = "data/database.json"
        self.item_list = DoublyLinkedList()
        
        self.load_data()  # Đọc dữ liệu từ file JSON lên RAM khi mở ứng dụng
        self.init_ui()     # Khởi tạo giao diện đồ họa
        self.refresh_table()

    def init_ui(self):
        # 1. Khung công cụ Tìm kiếm và Sắp xếp phía trên cùng
        top_frame = tk.Frame(self, pady=10)
        top_frame.pack(fill="x", padx=10)

        tk.Label(top_frame, text="Tìm kiếm (Tên/Mã):").pack(side="left", padx=2)
        self.txt_search = tk.Entry(top_frame, width=20)
        self.txt_search.pack(side="left", padx=5)
        tk.Button(top_frame, text="Tìm kiếm", command=self.search_item).pack(side="left", padx=2)

        tk.Label(top_frame, text="Sắp xếp theo:").pack(side="left", padx=20)
        self.cbo_sort = ttk.Combobox(top_frame, values=["Tên", "Giá", "Số lượng"], state="readonly", width=12)
        self.cbo_sort.set("Tên")
        self.cbo_sort.pack(side="left", padx=5)
        tk.Button(top_frame, text="Sắp xếp", command=self.sort_items).pack(side="left", padx=2)

        # 2. Bảng danh sách Treeview hiển thị dữ liệu hàng hóa
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Type", "Price", "Qty", "Extra"), show="headings")
        self.tree.heading("ID", text="Mã SP")
        self.tree.heading("Name", text="Tên sản phẩm")
        self.tree.heading("Type", text="Phân loại")
        self.tree.heading("Price", text="Giá Bán (Thuế)")
        self.tree.heading("Qty", text="Tồn kho")
        self.tree.heading("Extra", text="Thuộc tính riêng")
        
        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Price", width=120, anchor="e")
        self.tree.column("Qty", width=80, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # 3. Khung các nút chức năng bên dưới cùng
        btn_frame = tk.Frame(self, pady=10)
        btn_frame.pack(fill="x", padx=10)

        tk.Button(btn_frame, text="Thêm mặt hàng", command=self.add_item, width=15, bg="#2196F3", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Sửa đổi", command=self.edit_item, width=15, bg="#FF9800", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Xóa", command=self.delete_item, width=15, bg="#f44336", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Xem Thống kê", command=self.show_stats, width=15, bg="#9C27B0", fg="white").pack(side="right", padx=5)

    def refresh_table(self, custom_list=None):
        """Làm mới và đổ lại dữ liệu lên bảng hiển thị"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        display_list = custom_list if custom_list is not None else self.item_list.to_list()
        for item in display_list:
            extra_val = ""
            if hasattr(item, 'author'): extra_val = item.author
            elif hasattr(item, 'issue_number'): extra_val = item.issue_number
            elif hasattr(item, 'date'): extra_val = item.date
            elif hasattr(item, 'university'): extra_val = item.university
            elif hasattr(item, 'century'): extra_val = item.century
            
            self.tree.insert("", "end", values=(
                item.id, 
                item.name, 
                item.__class__.__name__, 
                f"{item.tinh_gia_ban():,.0f}đ", 
                item.quantity, 
                extra_val
            ))

    def add_item(self):
        """Chức năng thêm mới sản phẩm"""
        dialog = ItemDialog(self, "Thêm sản phẩm mới")
        self.wait_window(dialog)
        if dialog.result:
            res = dialog.result
            if self.item_list.search_by_id(res['id']):
                messagebox.showerror("Trùng lặp", "Mã sản phẩm này đã tồn tại trong hệ thống!")
                return
            
            t = res['type']
            if t == "Book": item = Book(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
            elif t == "Magazines": item = Magazines(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
            elif t == "Newspapers": item = Newspapers(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
            elif t == "Theses": item = Theses(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
            elif t == "Manuscripts": item = Manuscripts(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
            
            self.item_list.insert_tail(item)
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Thành công", "Đã lưu sản phẩm mới thành công!")

    def edit_item(self):
        """Chức năng chỉnh sửa thông tin"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa trên bảng.")
            return
        item_id = self.tree.item(selected[0])['values'][0]
        curr_item = self.item_list.search_by_id(str(item_id))
        
        extra_val = ""
        if hasattr(curr_item, 'author'): extra_val = curr_item.author
        elif hasattr(curr_item, 'issue_number'): extra_val = curr_item.issue_number
        elif hasattr(curr_item, 'date'): extra_val = curr_item.date
        elif hasattr(curr_item, 'university'): extra_val = curr_item.university
        elif hasattr(curr_item, 'century'): extra_val = curr_item.century

        item_data = {
            "id": curr_item.id, "name": curr_item.name, "type": curr_item.__class__.__name__,
            "base_price": curr_item.base_price, "quantity": curr_item.quantity, "extra": extra_val
        }

        dialog = ItemDialog(self, "Cập nhật sản phẩm", item_data)
        self.wait_window(dialog)
        if dialog.result:
            res = dialog.result
            curr_item.name = res['name']
            curr_item.base_price = res['base_price']
            curr_item.quantity = res['quantity']
            if hasattr(curr_item, 'author'): curr_item.author = res['extra']
            elif hasattr(curr_item, 'issue_number'): curr_item.issue_number = res['extra']
            elif hasattr(curr_item, 'date'): curr_item.date = res['extra']
            elif hasattr(curr_item, 'university'): curr_item.university = res['extra']
            elif hasattr(curr_item, 'century'): curr_item.century = res['extra']
            
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin thành công!")

    def delete_item(self):
        """Chức năng xóa sản phẩm"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm cần xóa.")
            return
        item_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Bạn chắc chắn muốn xóa mặt hàng mã {item_id}?"):
            self.item_list.remove_node(str(item_id))
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Thành công", "Đã xóa sản phẩm thành công.")

    def search_item(self):
        """Tìm kiếm thông minh: Tìm theo chính xác Mã SP hoặc theo Tên sản phẩm"""
        keyword = self.txt_search.get().strip().lower()
        if not keyword:
            self.refresh_table()
            return
        
        filtered = []
        curr = self.item_list.head
        while curr:
            # Kiểm tra nếu từ khóa khớp mã ID hoặc nằm trong Tên sản phẩm
            if keyword == curr.data.id.lower() or keyword in curr.data.name.lower():
                filtered.append(curr.data)
            curr = curr.next
        self.refresh_table(filtered)

    def sort_items(self):
        """Chức năng sắp xếp bằng thuật toán Merge Sort trên Linked List"""
        criteria_map = {"Tên": "name", "Giá": "price", "Số lượng": "quantity"}
        selected_criteria = criteria_map[self.cbo_sort.get()]
        self.item_list.sort_list(criteria=selected_criteria)
        self.refresh_table()

    def show_stats(self):
        """Chức năng xem báo cáo thống kê kho hàng"""
        all_items = self.item_list.to_list()
        if not all_items:
            messagebox.showinfo("Thống kê", "Hệ thống trống dữ liệu.")
            return
        total_qty = sum(item.quantity for item in all_items)
        most_expensive = max(all_items, key=lambda x: x.tinh_gia_ban())
        low_stock = [item.name for item in all_items if item.quantity < 5]

        msg = f"📊 KẾT QUẢ THỐNG KÊ:\n" \
              f"• Tổng số lượng mặt hàng đang có: {total_qty} sản phẩm.\n" \
              f"• Mặt hàng có giá cao nhất: {most_expensive.name} ({most_expensive.tinh_gia_ban():,.0f}đ)\n" \
              f"• Cảnh báo sắp hết hàng (SL < 5): {', '.join(low_stock) if low_stock else 'An toàn'}"
        messagebox.showinfo("Báo cáo", msg)

    def save_data(self):
        """Ghi dữ liệu xuống file JSON"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        data_to_save = []
        for item in self.item_list.to_list():
            extra_val = ""
            if hasattr(item, 'author'): extra_val = item.author
            elif hasattr(item, 'issue_number'): extra_val = item.issue_number
            elif hasattr(item, 'date'): extra_val = item.date
            elif hasattr(item, 'university'): extra_val = item.university
            elif hasattr(item, 'century'): extra_val = item.century
            
            data_to_save.append({
                "id": item.id, "name": item.name, "type": item.__class__.__name__,
                "base_price": item.base_price, "quantity": item.quantity, "extra": extra_val
            })
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    def load_data(self):
        """Đọc file JSON đưa vào cấu trúc dữ liệu RAM khi khởi động app"""
        if not os.path.exists(self.db_path):
            return
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data_list = json.load(f)
                for res in data_list:
                    t = res['type']
                    if t == "Book": item = Book(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
                    elif t == "Magazines": item = Magazines(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
                    elif t == "Newspapers": item = Newspapers(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
                    elif t == "Theses": item = Theses(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
                    elif t == "Manuscripts": item = Manuscripts(res['id'], res['name'], res['base_price'], res['quantity'], res['extra'])
                    self.item_list.insert_tail(item)
        except Exception as e:
            print("Lỗi tải database:", e)