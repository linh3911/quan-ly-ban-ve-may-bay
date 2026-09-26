import sys
import os

# Ép Python tìm kiếm trong thư mục hiện tại để tránh lỗi ModuleNotFoundError
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()