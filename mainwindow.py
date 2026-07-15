import sys
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)
from PySide6.QtGui import QBrush
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QWidget,
    QVBoxLayout,
    QPushButton,
)

from graphics_page import Graphics_Page


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.graphics = Graphics_Page()
        self.setCentralWidget(self.graphics)

        self.resize(1400, 800)

        self.setup_sidebar()

    def setup_sidebar(self):
        dock = QDockWidget("Experiments", self)
        dock.setFeatures(QDockWidget.DockWidgetMovable)

        container = QWidget()
        layout = QVBoxLayout(container)

        # Buttons
        step_btn = QPushButton("Step Prosaccade")
        gap_btn = QPushButton("Gap Prosaccade")
        overlap_btn = QPushButton("Overlap Prosaccade")
        pursuit_circle_btn = QPushButton("Smooth Pursuit: Circle")
        pursuit_figure8_btn = QPushButton("Smooth Pursuit: Figure 8")
        pursuit_horizontal_btn = QPushButton("Smooth Pursuit: Horizontal")

        layout.addWidget(step_btn)
        layout.addWidget(gap_btn)
        layout.addWidget(overlap_btn)
        layout.addWidget(pursuit_circle_btn)
        layout.addWidget(pursuit_figure8_btn)
        layout.addWidget(pursuit_horizontal_btn)
        layout.addStretch()

        # Connect signals
        step_btn.clicked.connect(self.graphics.step_prosaccade_run)
        gap_btn.clicked.connect(self.graphics.gap_prosaccade_run)
        overlap_btn.clicked.connect(self.graphics.overlap_prosaccade_run)
        pursuit_circle_btn.clicked.connect(self.graphics.smooth_pursuit_circle_run)
        pursuit_figure8_btn.clicked.connect(self.graphics.smooth_pursuit_figure8_run)
        pursuit_horizontal_btn.clicked.connect(self.graphics.smooth_pursuit_horizontal_run)

        dock.setWidget(container)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
    def send_signal(self):
        self.graphics.smooth_pursuit_run()
