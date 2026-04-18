#!/usr/bin/env python3

import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QTextEdit,
    QLabel, QAbstractItemView
)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont

# Import Lõi GA
from robot_omni.gui.ga_core import run_genetic_algorithm, load_distance_matrix, route_distance

ROOMS = [f"Phong_{i}" for i in range(1, 25)]

# ================================
# THREAD CHẠY GA PREVIEW
# ================================
class GAThread(QThread):
    finished_signal = pyqtSignal(list, float)

    def __init__(self, rooms):
        super().__init__()
        self.rooms = rooms

    def run(self):
        try:
            matrix = load_distance_matrix()
            route = run_genetic_algorithm(self.rooms, distance_matrix=matrix)
            distance = route_distance(route, matrix)
            self.finished_signal.emit(route, distance)
        except Exception as e:
            print(f"Lỗi khi chạy GA Preview: {e}")

# ================================
# MAIN GUI
# ================================
class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 GA Robot Planner PRO")
        self.setGeometry(100, 100, 1100, 600)

        self.setStyleSheet("""
            QWidget { background-color: #1e1e1e; color: #ffffff; font-size: 14px; }
            QPushButton { background-color: #007acc; border-radius: 10px; padding: 10px; }
            QPushButton:hover { background-color: #005f99; }
            QListWidget { background-color: #2b2b2b; }
            QTextEdit { background-color: #2b2b2b; }
        """)

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # -------- LEFT PANEL --------
        left_layout = QVBoxLayout()
        title = QLabel("📍 Danh sách phòng")
        title.setFont(QFont("Arial", 16))

        self.room_list = QListWidget()
        self.room_list.setSelectionMode(QAbstractItemView.MultiSelection)
        for room in ROOMS:
            self.room_list.addItem(room)

        self.btn_run = QPushButton("▶ Preview GA (Dự kiến)")
        self.btn_run.clicked.connect(self.run_ga)

        self.btn_start = QPushButton("🚀 Thực thi Robot (ROS 2)")
        self.btn_start.setStyleSheet("background-color: #28a745;")
        self.btn_start.clicked.connect(self.start_robot)

        self.btn_clear = QPushButton("🗑 Clear Log")
        self.btn_clear.clicked.connect(self.clear_log)

        left_layout.addWidget(title)
        left_layout.addWidget(self.room_list)
        left_layout.addWidget(self.btn_run)
        left_layout.addWidget(self.btn_start)
        left_layout.addWidget(self.btn_clear)

        # -------- RIGHT PANEL --------
        right_layout = QVBoxLayout()
        self.route_label = QLabel("Route: ...")
        self.route_label.setFont(QFont("Arial", 14))
        self.route_label.setWordWrap(True)

        self.distance_label = QLabel("Distance: ...")
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        right_layout.addWidget(self.route_label)
        right_layout.addWidget(self.distance_label)
        right_layout.addWidget(self.log_box)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def log(self, text):
        self.log_box.append(text)

    def get_selected_rooms(self):
        return [item.text() for item in self.room_list.selectedItems()]

    def run_ga(self):
        rooms = self.get_selected_rooms()
        if not rooms:
            self.log("⚠️ Chưa chọn phòng")
            return
        self.log("⏳ Đang tính toán Preview...")
        self.thread = GAThread(rooms)
        self.thread.finished_signal.connect(self.on_ga_done)
        self.thread.start()

    def on_ga_done(self, route, distance):
        self.route_label.setText("Route: " + " → ".join(route))
        self.distance_label.setText(f"Distance: {distance:.2f} m")
        self.log("✅ Preview xong. (Lưu ý: Robot sẽ tự tính lại trạm đầu tiên cho gần nhất)")

    def start_robot(self):
        rooms = self.get_selected_rooms()
        if not rooms:
            self.log("⚠️ Chưa chọn phòng")
            return

        self.log("🚀 Đang khởi động tiến trình Node ROS 2...")
        try:
            # Gửi danh sách phòng qua file nav_controller.py
            route_str = ",".join(rooms)
            subprocess.Popen(["python3", "nav_controller.py", route_str])
            self.log(f"✅ Đã gửi lệnh cho robot: {route_str}")
        except Exception as e:
            self.log(f"❌ Lỗi: {e}")

    def clear_log(self):
        self.log_box.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())