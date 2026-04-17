# #!/usr/bin/env python3

# import sys
# import os
# import subprocess
# import re
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QWidget,
#     QVBoxLayout, QHBoxLayout,
#     QPushButton, QListWidget, QTextEdit,
#     QLabel, QScrollArea, QFrame, QComboBox
# )
# from PyQt5.QtCore import QThread, pyqtSignal, Qt
# from PyQt5.QtGui import QFont, QPixmap, QTextCursor

# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# if CURRENT_DIR not in sys.path:
#     sys.path.insert(0, CURRENT_DIR)

# # Import Lõi GA
# try:
#     from ga_core import run_genetic_algorithm, load_distance_matrix, route_distance
# except ImportError as e:
#     def run_genetic_algorithm(*args, **kwargs): return []
#     def load_distance_matrix(): return {}
#     def route_distance(*args): return 0.0
#     print(f"[!] Cảnh báo: Không tìm thấy file ga_core.py: {e}")

# ROOMS = [f"Phong_{i}" for i in range(1, 25)]

# ROOM_PIXELS = {
#     'Phong_1': (70, 165),  'Phong_2': (130, 80),  'Phong_3': (205, 50),  'Phong_4': (275, 50),
#     'Phong_5': (420, 70),  'Phong_6': (365, 120),  'Phong_7': (680, 70),  'Phong_8': (605, 120),
#     'Phong_9': (880, 200),  'Phong_10': (710, 220), 'Phong_11': (710, 280), 'Phong_12': (578, 220),
#     'Phong_13': (578, 280), 'Phong_14': (430, 230), 'Phong_15': (430, 280), 'Phong_16': (70, 339),
#     'Phong_17': (130, 421), 'Phong_18': (205, 450), 'Phong_19': (275, 450), 'Phong_20': (420, 430),
#     'Phong_21': (365, 385), 'Phong_22': (680, 430), 'Phong_23': (605, 385), 'Phong_24': (880, 430),
# }

# ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# class ProcessOutputReader(QThread):
#     output_signal = pyqtSignal(str)

#     def __init__(self, process):
#         super().__init__()
#         self.process = process

#     def run(self):
#         for line in iter(self.process.stdout.readline, ''):
#             if line:
#                 clean_line = ANSI_ESCAPE.sub('', line.strip())
#                 self.output_signal.emit(clean_line)
#         self.process.stdout.close()

# # Đã sửa: Truyền thêm biến mode vào thread
# class RouteThread(QThread):
#     finished_signal = pyqtSignal(list, float)

#     def __init__(self, rooms, mode):
#         super().__init__()
#         self.rooms = rooms
#         self.mode = mode

#     def run(self):
#         try:
#             matrix = load_distance_matrix()
#             if self.mode == "ga":
#                 route = run_genetic_algorithm(self.rooms, distance_matrix=matrix)
#             else:
#                 # Chế độ tuần tự: Giữ nguyên thứ tự danh sách
#                 route = list(self.rooms) 
                
#             distance = route_distance(route, matrix)
#             self.finished_signal.emit(route, distance)
#         except Exception as e:
#             print(f"Lỗi khi chạy Preview: {e}")

# class MapButton(QPushButton):
#     def __init__(self, room_name, parent_map):
#         room_num = room_name.split("_")[1]
#         super().__init__(room_num, parent_map)
        
#         self.room_name = room_name
#         self.is_selected = False
        
#         self.setFixedSize(32, 32)
#         self.setFont(QFont("Segoe UI", 10, QFont.Bold))
#         self.setCursor(Qt.PointingHandCursor)
#         self.update_style()

#     def toggle_selection(self):
#         self.is_selected = not self.is_selected
#         self.update_style()
#         return self.is_selected

#     def update_style(self):
#         if self.is_selected:
#             self.setStyleSheet("QPushButton { background-color: #2ecc71; color: white; border: 2px solid #ffffff; border-radius: 16px; }")
#         else:
#             self.setStyleSheet("QPushButton { background-color: rgba(231, 76, 60, 0.8); color: white; border: 1px solid #ffffff; border-radius: 16px; } QPushButton:hover { background-color: #e74c3c; border: 2px solid #fff; }")

# class GUI(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Hệ Thống Điều Phối Robot Bệnh Viện (FMS)")
#         self.setGeometry(100, 50, 1400, 700)
#         QApplication.setStyle("Fusion")
        
#         self.setStyleSheet("""
#             QWidget { background-color: #1e1e2e; color: #cdd6f4; font-family: 'Segoe UI', Arial; font-size: 14px; }
#             QScrollArea { border: none; background-color: #181825; }
#             QLabel { color: #cdd6f4; }
#         """)

#         self.selected_rooms = []
#         self.map_buttons = {}
#         self.nav_process = None
#         self.log_reader_thread = None

#         self.init_ui()

#     def init_ui(self):
#         main_layout = QHBoxLayout()
#         main_layout.setContentsMargins(15, 15, 15, 15)
#         main_layout.setSpacing(20)

#         map_container = QWidget()
#         map_container.setFixedSize(1000, 500) 
        
#         self.map_label = QLabel(map_container)
#         self.map_label.setGeometry(0, 0, 1000, 500)
#         self.map_label.setStyleSheet("background-color: #313244; border-radius: 10px;")
        
#         map_image_path = os.path.join(CURRENT_DIR, "map_hospital.jpg")
#         if os.path.exists(map_image_path):
#             pixmap = QPixmap(map_image_path).scaled(1000, 500, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
#             self.map_label.setPixmap(pixmap)
#         else:
#             self.map_label.setText(f"[!] KHÔNG TÌM THẤY ẢNH TẠI:\n{map_image_path}")
#             self.map_label.setAlignment(Qt.AlignCenter)
#             self.map_label.setStyleSheet("border: 2px dashed #f38ba8; color: #f38ba8; background-color: #181825;")

#         for room in ROOMS:
#             btn = MapButton(room, map_container)
#             if room in ROOM_PIXELS:
#                 x, y = ROOM_PIXELS[room]
#                 btn.move(x - 16, y - 16) 
#             btn.clicked.connect(lambda checked, r=room: self.on_map_button_clicked(r))
#             self.map_buttons[room] = btn

#         scroll_area = QScrollArea()
#         scroll_area.setWidget(map_container)
#         scroll_area.setAlignment(Qt.AlignCenter)

#         right_panel = QFrame()
#         right_panel.setFixedWidth(380)
#         right_panel.setStyleSheet("""
#             QFrame { background-color: #181825; border-radius: 10px; }
#             QPushButton { border-radius: 8px; font-weight: bold; padding: 10px; font-size: 14px; border: none; }
#             QComboBox { background-color: #313244; border: 1px solid #45475a; border-radius: 8px; padding: 8px; font-weight: bold;}
#             QComboBox::drop-down { border: none; }
#         """)
#         right_layout = QVBoxLayout(right_panel)
#         right_layout.setSpacing(12)

#         header = QLabel("BẢNG ĐIỀU KHIỂN")
#         header.setFont(QFont("Segoe UI", 16, QFont.Bold))
#         header.setAlignment(Qt.AlignCenter)
#         header.setStyleSheet("color: #89b4fa; padding-bottom: 5px;")
        
#         # --- THÊM CHỌN CHẾ ĐỘ ---
#         self.mode_selector = QComboBox()
#         self.mode_selector.addItems([
#             "🧠 Chế độ: Tối ưu lộ trình (GA)", 
#             "🔢 Chế độ: Chạy theo thứ tự chọn"
#         ])
        
#         self.btn_clear_map = QPushButton("✖  Xóa chọn tất cả")
#         self.btn_clear_map.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; } QPushButton:hover { background-color: #e6456f; }")
#         self.btn_clear_map.clicked.connect(self.clear_selection)

#         self.btn_run = QPushButton("▶  Xem trước lộ trình")
#         self.btn_run.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; } QPushButton:hover { background-color: #74c7ec; }")
#         self.btn_run.clicked.connect(self.run_preview)

#         self.btn_start = QPushButton("►  THỰC THI ROBOT")
#         self.btn_start.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; font-size: 16px; padding: 15px; } QPushButton:hover { background-color: #94e2d5; }")
#         self.btn_start.clicked.connect(self.start_robot)

#         self.route_label = QLabel("• Lộ trình: Chưa tính toán")
#         self.route_label.setWordWrap(True)
#         self.route_label.setStyleSheet("color: #f9e2af; font-size: 14px; font-weight: bold;")
        
#         self.distance_label = QLabel("• Quãng đường: 0.0 m")
#         self.distance_label.setStyleSheet("color: #fab387; font-size: 14px; font-weight: bold;")
        
#         log_label = QLabel("• LOG TRẠNG THÁI ROS 2:")
#         log_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        
#         self.log_box = QTextEdit()
#         self.log_box.setReadOnly(True)
#         self.log_box.setStyleSheet("""
#             QTextEdit { background-color: #11111b; color: #a6adc8; border: 1px solid #45475a; border-radius: 8px; padding: 5px; font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; }
#         """)

#         right_layout.addWidget(header)
#         right_layout.addWidget(self.mode_selector) # Thêm UI vào Layout
#         right_layout.addWidget(self.btn_clear_map)
#         right_layout.addWidget(self.btn_run)
#         right_layout.addWidget(self.btn_start)
#         right_layout.addWidget(QLabel("<hr style='background-color:#45475a;'>"))
#         right_layout.addWidget(self.route_label)
#         right_layout.addWidget(self.distance_label)
#         right_layout.addWidget(log_label)
#         right_layout.addWidget(self.log_box)

#         main_layout.addWidget(scroll_area)
#         main_layout.addWidget(right_panel)

#         container = QWidget()
#         container.setLayout(main_layout)
#         self.setCentralWidget(container)

#     def log(self, text):
#         self.log_box.append(text)
#         self.log_box.moveCursor(QTextCursor.End)

#     def on_map_button_clicked(self, room_name):
#         btn = self.map_buttons[room_name]
#         is_selected = btn.toggle_selection()
        
#         if is_selected:
#             self.selected_rooms.append(room_name)
#             self.log(f"> [+] Đã chọn (Vị trí {len(self.selected_rooms)}): {room_name}")
#         else:
#             if room_name in self.selected_rooms:
#                 self.selected_rooms.remove(room_name)
#                 self.log(f"> [-] Đã bỏ chọn: {room_name}")

#     def clear_selection(self):
#         self.selected_rooms.clear()
#         for btn in self.map_buttons.values():
#             btn.is_selected = False
#             btn.update_style()
#         self.log("> [✖] Đã xóa toàn bộ điểm đến.")
#         self.route_label.setText("• Lộ trình: Chưa tính toán")
#         self.distance_label.setText("• Quãng đường: 0.0 m")

#     def run_preview(self):
#         if not self.selected_rooms:
#             self.log("> [!] Hãy chọn ít nhất 1 phòng trên bản đồ!")
#             return
            
#         mode = "ga" if self.mode_selector.currentIndex() == 0 else "sequential"
#         mode_text = "Tối ưu GA" if mode == "ga" else "Thứ tự"
        
#         self.log(f"> [...] Đang tính toán xem trước ({mode_text})...")
#         self.thread = RouteThread(self.selected_rooms, mode)
#         self.thread.finished_signal.connect(self.on_preview_done)
#         self.thread.start()

#     def on_preview_done(self, route, distance):
#         if not route: return
#         clean_route = [r.replace("Phong_", "") for r in route]
#         self.route_label.setText("• Lộ trình dự kiến: " + " → ".join(clean_route))
#         self.distance_label.setText(f"• Quãng đường dự kiến: {distance:.2f} m")
#         self.log("> [✔] Xem trước tính toán xong.")

#     def start_robot(self):
#         if not self.selected_rooms:
#             self.log("> [!] Chưa có phòng nào được chọn để di chuyển!")
#             return
            
#         if self.nav_process and self.nav_process.poll() is None:
#             self.log("> [■] Đang dừng tiến trình robot cũ...")
#             self.nav_process.terminate()
#             self.nav_process.wait()

#         mode = "ga" if self.mode_selector.currentIndex() == 0 else "sequential"

#         self.log("\n==================================")
#         self.log(f"> [►] BẮT ĐẦU GỬI LỆNH XUỐNG ROBOT (Chế độ: {mode.upper()})...")
#         self.log("==================================")
        
#         try:
#             route_str = ",".join(self.selected_rooms)
#             self.nav_process = subprocess.Popen(
#                 ["python3", "-u", "nav_controller.py", route_str, mode], # Truyền thêm mode
#                 cwd=CURRENT_DIR,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.STDOUT,
#                 text=True
#             )
            
#             self.log_reader_thread = ProcessOutputReader(self.nav_process)
#             self.log_reader_thread.output_signal.connect(self.log)
#             self.log_reader_thread.start()
            
#         except Exception as e:
#             self.log(f"> [✖] Lỗi khởi chạy: {e}")

#     def closeEvent(self, event):
#         if self.nav_process and self.nav_process.poll() is None:
#             self.nav_process.terminate()
#         event.accept()

# if __name__ == "__main__":
#     os.environ["GTK_PATH"] = ""
#     app = QApplication(sys.argv)
#     window = GUI()
#     window.show()
#     sys.exit(app.exec_())




#!/usr/bin/env python3

import sys
import os
import subprocess
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QTextEdit,
    QLabel, QScrollArea, QFrame, QComboBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPixmap, QTextCursor

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# Import Lõi GA
try:
    from ga_core import run_genetic_algorithm, load_distance_matrix, route_distance
except ImportError as e:
    def run_genetic_algorithm(*args, **kwargs): return []
    def load_distance_matrix(): return {}
    def route_distance(*args): return 0.0
    print(f"[!] Cảnh báo: Không tìm thấy file ga_core.py: {e}")

ROOMS = [f"Phong_{i}" for i in range(1, 25)]

ROOM_PIXELS = {
    'Phong_1': (70, 165),  'Phong_2': (130, 80),  'Phong_3': (205, 50),  'Phong_4': (275, 50),
    'Phong_5': (420, 70),  'Phong_6': (365, 120),  'Phong_7': (680, 70),  'Phong_8': (605, 120),
    'Phong_9': (880, 200),  'Phong_10': (710, 220), 'Phong_11': (710, 280), 'Phong_12': (578, 220),
    'Phong_13': (578, 280), 'Phong_14': (430, 230), 'Phong_15': (430, 280), 'Phong_16': (70, 339),
    'Phong_17': (130, 421), 'Phong_18': (205, 450), 'Phong_19': (275, 450), 'Phong_20': (420, 430),
    'Phong_21': (365, 385), 'Phong_22': (680, 430), 'Phong_23': (605, 385), 'Phong_24': (880, 430),
}

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

class ProcessOutputReader(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, process):
        super().__init__()
        self.process = process

    def run(self):
        for line in iter(self.process.stdout.readline, ''):
            if line:
                clean_line = ANSI_ESCAPE.sub('', line.strip())
                self.output_signal.emit(clean_line)
        self.process.stdout.close()

class RouteThread(QThread):
    finished_signal = pyqtSignal(list, float)

    def __init__(self, rooms, mode):
        super().__init__()
        self.rooms = rooms
        self.mode = mode

    def run(self):
        try:
            matrix = load_distance_matrix()
            if self.mode == "ga":
                route = run_genetic_algorithm(self.rooms, distance_matrix=matrix)
            else:
                # Chế độ tuần tự: Giữ nguyên y xì thứ tự click của người dùng
                route = list(self.rooms) 
                
            distance = route_distance(route, matrix)
            self.finished_signal.emit(route, distance)
        except Exception as e:
            print(f"Lỗi khi chạy Preview: {e}")

class MapButton(QPushButton):
    def __init__(self, room_name, parent_map):
        room_num = room_name.split("_")[1]
        super().__init__(room_num, parent_map)
        
        self.room_name = room_name
        self.is_selected = False
        
        self.setFixedSize(32, 32)
        self.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()

    def toggle_selection(self):
        self.is_selected = not self.is_selected
        self.update_style()
        return self.is_selected

    def update_style(self):
        if self.is_selected:
            self.setStyleSheet("QPushButton { background-color: #2ecc71; color: white; border: 2px solid #ffffff; border-radius: 16px; }")
        else:
            self.setStyleSheet("QPushButton { background-color: rgba(231, 76, 60, 0.8); color: white; border: 1px solid #ffffff; border-radius: 16px; } QPushButton:hover { background-color: #e74c3c; border: 2px solid #fff; }")

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Điều Phối Robot Bệnh Viện (FMS)")
        self.setGeometry(100, 50, 1400, 700)
        QApplication.setStyle("Fusion")
        
        self.setStyleSheet("""
            QWidget { background-color: #1e1e2e; color: #cdd6f4; font-family: 'Segoe UI', Arial; font-size: 14px; }
            QScrollArea { border: none; background-color: #181825; }
            QLabel { color: #cdd6f4; }
        """)

        self.selected_rooms = []
        self.map_buttons = {}
        self.nav_process = None
        self.log_reader_thread = None

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)

        map_container = QWidget()
        map_container.setFixedSize(1000, 500) 
        
        self.map_label = QLabel(map_container)
        self.map_label.setGeometry(0, 0, 1000, 500)
        self.map_label.setStyleSheet("background-color: #313244; border-radius: 10px;")
        
        map_image_path = os.path.join(CURRENT_DIR, "map_hospital.jpg")
        if os.path.exists(map_image_path):
            pixmap = QPixmap(map_image_path).scaled(1000, 500, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.map_label.setPixmap(pixmap)
        else:
            self.map_label.setText(f"[!] KHÔNG TÌM THẤY ẢNH TẠI:\n{map_image_path}")
            self.map_label.setAlignment(Qt.AlignCenter)
            self.map_label.setStyleSheet("border: 2px dashed #f38ba8; color: #f38ba8; background-color: #181825;")

        for room in ROOMS:
            btn = MapButton(room, map_container)
            if room in ROOM_PIXELS:
                x, y = ROOM_PIXELS[room]
                btn.move(x - 16, y - 16) 
            btn.clicked.connect(lambda checked, r=room: self.on_map_button_clicked(r))
            self.map_buttons[room] = btn

        scroll_area = QScrollArea()
        scroll_area.setWidget(map_container)
        scroll_area.setAlignment(Qt.AlignCenter)

        right_panel = QFrame()
        right_panel.setFixedWidth(380)
        right_panel.setStyleSheet("""
            QFrame { background-color: #181825; border-radius: 10px; }
            QPushButton { border-radius: 8px; font-weight: bold; padding: 10px; font-size: 14px; border: none; }
            QComboBox { background-color: #313244; border: 1px solid #45475a; border-radius: 8px; padding: 8px; font-weight: bold;}
            QComboBox::drop-down { border: none; }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(12)

        header = QLabel("BẢNG ĐIỀU KHIỂN")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #89b4fa; padding-bottom: 5px;")
        
        # --- ĐÃ FIX LỖI FONT ICON ---
        self.mode_selector = QComboBox()
        self.mode_selector.addItems([
            "◈ Chế độ: Tối ưu lộ trình (GA)", 
            "☷ Chế độ: Chạy theo thứ tự chọn"
        ])
        
        self.btn_clear_map = QPushButton("✖  Xóa chọn tất cả")
        self.btn_clear_map.setStyleSheet("QPushButton { background-color: #f38ba8; color: #11111b; } QPushButton:hover { background-color: #e6456f; }")
        self.btn_clear_map.clicked.connect(self.clear_selection)

        self.btn_run = QPushButton("▶  Xem trước lộ trình")
        self.btn_run.setStyleSheet("QPushButton { background-color: #89b4fa; color: #11111b; } QPushButton:hover { background-color: #74c7ec; }")
        self.btn_run.clicked.connect(self.run_preview)

        self.btn_start = QPushButton("►  THỰC THI ROBOT")
        self.btn_start.setStyleSheet("QPushButton { background-color: #a6e3a1; color: #11111b; font-size: 16px; padding: 15px; } QPushButton:hover { background-color: #94e2d5; }")
        self.btn_start.clicked.connect(self.start_robot)

        self.route_label = QLabel("• Lộ trình: Chưa tính toán")
        self.route_label.setWordWrap(True)
        self.route_label.setStyleSheet("color: #f9e2af; font-size: 14px; font-weight: bold;")
        
        self.distance_label = QLabel("• Quãng đường: 0.0 m")
        self.distance_label.setStyleSheet("color: #fab387; font-size: 14px; font-weight: bold;")
        
        log_label = QLabel("• LOG TRẠNG THÁI ROS 2:")
        log_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("""
            QTextEdit { background-color: #11111b; color: #a6adc8; border: 1px solid #45475a; border-radius: 8px; padding: 5px; font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; }
        """)

        right_layout.addWidget(header)
        right_layout.addWidget(self.mode_selector)
        right_layout.addWidget(self.btn_clear_map)
        right_layout.addWidget(self.btn_run)
        right_layout.addWidget(self.btn_start)
        right_layout.addWidget(QLabel("<hr style='background-color:#45475a;'>"))
        right_layout.addWidget(self.route_label)
        right_layout.addWidget(self.distance_label)
        right_layout.addWidget(log_label)
        right_layout.addWidget(self.log_box)

        main_layout.addWidget(scroll_area)
        main_layout.addWidget(right_panel)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def log(self, text):
        self.log_box.append(text)
        self.log_box.moveCursor(QTextCursor.End)

    def on_map_button_clicked(self, room_name):
        btn = self.map_buttons[room_name]
        is_selected = btn.toggle_selection()
        
        if is_selected:
            self.selected_rooms.append(room_name)
            self.log(f"> [+] Đã chọn (Vị trí số {len(self.selected_rooms)}): {room_name}")
        else:
            if room_name in self.selected_rooms:
                self.selected_rooms.remove(room_name)
                self.log(f"> [-] Đã bỏ chọn: {room_name}")

    def clear_selection(self):
        self.selected_rooms.clear()
        for btn in self.map_buttons.values():
            btn.is_selected = False
            btn.update_style()
        self.log("> [✖] Đã xóa toàn bộ điểm đến.")
        self.route_label.setText("• Lộ trình: Chưa tính toán")
        self.distance_label.setText("• Quãng đường: 0.0 m")

    def run_preview(self):
        if not self.selected_rooms:
            self.log("> [!] Hãy chọn ít nhất 1 phòng trên bản đồ!")
            return
            
        mode = "ga" if self.mode_selector.currentIndex() == 0 else "sequential"
        mode_text = "Tối ưu GA" if mode == "ga" else "Thứ tự"
        
        self.log(f"> [...] Đang tính toán xem trước ({mode_text})...")
        self.thread = RouteThread(self.selected_rooms, mode)
        self.thread.finished_signal.connect(self.on_preview_done)
        self.thread.start()

    def on_preview_done(self, route, distance):
        if not route: return
        clean_route = [r.replace("Phong_", "") for r in route]
        mode = self.mode_selector.currentIndex()
        
        # Cập nhật text để làm rõ ý nghĩa của preview
        if mode == 0:
            self.route_label.setText("• GA ước lượng (chưa tính vị trí Robot):\n  " + " → ".join(clean_route))
        else:
            self.route_label.setText("• Lộ trình theo đúng thứ tự chọn:\n  " + " → ".join(clean_route))
            
        self.distance_label.setText(f"• Quãng đường: {distance:.2f} m")
        self.log("> [✔] Xem trước tính toán xong.")

    def start_robot(self):
        if not self.selected_rooms:
            self.log("> [!] Chưa có phòng nào được chọn để di chuyển!")
            return
            
        if self.nav_process and self.nav_process.poll() is None:
            self.log("> [■] Đang dừng tiến trình robot cũ...")
            self.nav_process.terminate()
            self.nav_process.wait()

        mode = "ga" if self.mode_selector.currentIndex() == 0 else "sequential"

        self.log("\n==================================")
        self.log(f"> [►] BẮT ĐẦU GỬI LỆNH XUỐNG ROBOT (Chế độ: {mode.upper()})...")
        self.log("==================================")
        
        try:
            route_str = ",".join(self.selected_rooms)
            self.nav_process = subprocess.Popen(
                ["python3", "-u", "nav_controller.py", route_str, mode], 
                cwd=CURRENT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            self.log_reader_thread = ProcessOutputReader(self.nav_process)
            self.log_reader_thread.output_signal.connect(self.log)
            self.log_reader_thread.start()
            
        except Exception as e:
            self.log(f"> [✖] Lỗi khởi chạy: {e}")

    def closeEvent(self, event):
        if self.nav_process and self.nav_process.poll() is None:
            self.nav_process.terminate()
        event.accept()

if __name__ == "__main__":
    os.environ["GTK_PATH"] = ""
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())