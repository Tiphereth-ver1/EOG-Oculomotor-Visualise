import sys
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)
from PySide6.QtGui import QBrush
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit
)

from Trial import Experiment
from graphics_page import Graphics_Page
from data_logger import Data_Logger
from Connection import Serial_Worker

class MainWindow(QMainWindow):
    connection_request = Signal()
    def __init__(self):
        super().__init__()

        self.graphics = Graphics_Page()
        self.setCentralWidget(self.graphics)
        self.experiment : Experiment = Experiment()
        self.logger : Data_Logger = Data_Logger()
        self.conn = Serial_Worker()

        self.conn_thread = QThread()
        self.conn.moveToThread(self.conn_thread)

        self.connection_request.connect(self.conn.connect_port)

        self.conn.connection_status.connect(self.status_message)

        self.conn_thread.start()        
        self.status = False
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
        connect_btn = QPushButton("Connect")
        status_btn = QPushButton("Debug")
        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)

        layout.addWidget(expt_btn)
        layout.addStretch()
        layout.addWidget(connect_btn)
        layout.addWidget(status_btn)
        layout.addWidget(self.status_box)
        self.status_box.hide()

        # Connect signals
        expt_btn.clicked.connect(self.expt_start)
        status_btn.clicked.connect(self.toggle_status)
        connect_btn.clicked.connect(self.connection_request.emit)


        dock.setWidget(container)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def expt_start(self):
        self.logger.write_message("Experimental battery started.")
        self.experiment.start(self.graphics.fixation, self.graphics.target)
    
    def toggle_status(self):
        self.status = not self.status
        if self.status:
            self.status_box.show()
        if not self.status:
            self.status_box.hide()
    
    def status_message(self, message):
        self.status_box.append(message)
