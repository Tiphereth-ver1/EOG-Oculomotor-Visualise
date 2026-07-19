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

from Trial import Experiment
from graphics_page import Graphics_Page
from data_logger import Data_Logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.graphics = Graphics_Page()
        self.setCentralWidget(self.graphics)
        self.experiment : Experiment = Experiment()
        self.logger : Data_Logger = Data_Logger()

        self.experiment.logger_message.connect(self.logger.write_message)

        self.experiment.show_title.connect(self.graphics.show_title)
        self.experiment.show_instruction.connect(self.graphics.show_instruction)
        self.experiment.clear_text.connect(self.graphics.clear_text)

        self.resize(1400, 800)

        self.setup_sidebar()

    def setup_sidebar(self):
        dock = QDockWidget("Experiments", self)
        dock.setFeatures(QDockWidget.DockWidgetMovable)

        container = QWidget()
        layout = QVBoxLayout(container)

        # Buttons
        expt_btn = QPushButton("Experiment")

        layout.addWidget(expt_btn)
        layout.addStretch()

        # Connect signals
        expt_btn.clicked.connect(self.expt_start)

        dock.setWidget(container)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def expt_start(self):
        self.logger.write_message("Experimental battery started.")
        self.experiment.start(self.graphics.fixation, self.graphics.target)
    
