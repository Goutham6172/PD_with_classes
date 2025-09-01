from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QWidget, QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QBrush, QColor, QPainter
from PySide6.QtCore import Qt, QPointF
import sys
import math


class TargetPlotter:
    def __init__(self, scene):
        self.scene = scene
        self.targets_A = {}
        self.targets_B = {}

    def polar_to_cartesian(self, range_val, azimuth_deg):
        angle_rad = math.radians(azimuth_deg)
        x = range_val * math.cos(angle_rad)
        y = -range_val * math.sin(angle_rad)  # Negative Y for top-down display
        return x, y

    def create_target_item(self, target):
        x, y = self.polar_to_cartesian(target['range'], target['azimuth'])
        dot = QGraphicsEllipseItem(-4, -4, 8, 8)
        dot.setBrush(QBrush(QColor("red") if target['category'] == 'A' else QColor("blue")))
        dot.setPos(x, y)
        dot.setZValue(1)
        return dot

    def update_targets(self, targets):
        # Clear existing items
        for item in self.targets_A.values():
            self.scene.removeItem(item)
        for item in self.targets_B.values():
            self.scene.removeItem(item)
        self.targets_A.clear()
        self.targets_B.clear()

        # Add new items
        for t in targets:
            item = self.create_target_item(t)
            if t['category'] == 'A':
                self.targets_A[t['id']] = item
            else:
                self.targets_B[t['id']] = item
            self.scene.addItem(item)

    def show_targets(self, category, visible):
        group = self.targets_A if category == 'A' else self.targets_B
        for item in group.values():
            item.setVisible(visible)

    def show_all(self, visible=True):
        for item in self.targets_A.values():
            item.setVisible(visible)
        for item in self.targets_B.values():
            item.setVisible(visible)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polar Display - Target Categories")
        self.setGeometry(200, 200, 800, 600)

        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Graphics view/scene
        self.scene = QGraphicsScene(-300, -300, 600, 600)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        main_layout.addWidget(self.view)

        # Buttons
        button_layout = QHBoxLayout()
        self.btn_cat_a = QPushButton("Show Category A")
        self.btn_cat_b = QPushButton("Show Category B")
        self.btn_both = QPushButton("Show Both")
        button_layout.addWidget(self.btn_cat_a)
        button_layout.addWidget(self.btn_cat_b)
        button_layout.addWidget(self.btn_both)
        main_layout.addLayout(button_layout)

        # Plotter
        self.target_plotter = TargetPlotter(self.scene)

        # Button connections
        self.btn_cat_a.clicked.connect(lambda: self.show_category('A'))
        self.btn_cat_b.clicked.connect(lambda: self.show_category('B'))
        self.btn_both.clicked.connect(lambda: self.show_category('Both'))

        # Mock data
        self.load_mock_targets()

    def show_category(self, cat):
        if cat == 'A':
            self.target_plotter.show_targets('A', True)
            self.target_plotter.show_targets('B', False)
        elif cat == 'B':
            self.target_plotter.show_targets('A', False)
            self.target_plotter.show_targets('B', True)
        elif cat == 'Both':
            self.target_plotter.show_all(True)

    def load_mock_targets(self):
        targets = []
        for i in range(10):
            targets.append({'id': f'A{i}', 'range': 50 + i*10, 'azimuth': i * 10, 'category': 'A'})
        for i in range(10):
            targets.append({'id': f'B{i}', 'range': 60 + i*10, 'azimuth': i * 15 + 5, 'category': 'B'})
        self.target_plotter.update_targets(targets)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

# https://1drv.ms/w/c/fd9c3d82ca06da8b/EbNd5EqlnKlEr2a-YnFYdLkBcDS9DQJw4vcILXQy2tzNig?e=un3PCJ
# https://1drv.ms/w/c/fd9c3d82ca06da8b/Ed2G0R9g5YVGrBB-oZjEpNABxur3pGtAphdJd7wSkxXyWA?e=KdZsqm
