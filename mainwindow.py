import sys
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QFormLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)
from PySide6.QtGui import QBrush, QFont
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel
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
        self.experiment.updating_exp.connect(self.update_exp_status)
        self.experiment.updating_reps.connect(self.update_rep_status)
        self.experiment.enable_pause.connect(self.enable_pause)
        self.experiment.disable_pause.connect(self.diable_pause)
        self.experiment.event_sent.connect(self.logger.add_event)
        self.experiment.experiment_complete.connect(self.logger.save)

        self.resize(1400, 800)

        self.setup_sidebar()

    def setup_sidebar(self):
        self.dock = QDockWidget("Experiments", self)
        self.dock.setFeatures(QDockWidget.DockWidgetMovable)

        container = QWidget()
        layout = QVBoxLayout(container)


        # Buttons
        expt_btn = QPushButton("Experiment")
        self.countdown_btn = QPushButton("Pause")
        self.countdown_btn.setEnabled(False)
        connect_btn = QPushButton("Connect")
        status_btn = QPushButton("Debug")
        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)

        self.make_info_box()

        layout.addWidget(expt_btn)
        layout.addWidget(self.countdown_btn)
        layout.addWidget(self.info)
        layout.addStretch()
        layout.addWidget(connect_btn)
        layout.addWidget(status_btn)
        layout.addWidget(self.status_box)
        self.status_box.hide()
        self.status_box.setFixedWidth(150)

        # Connect signals
        expt_btn.clicked.connect(self.expt_start)
        expt_btn.clicked.connect(self.logger.init_main_data)
        self.countdown_btn.clicked.connect(self.countdowner)
        status_btn.clicked.connect(self.toggle_status)
        connect_btn.clicked.connect(self.connection_request.emit)


        self.dock.setWidget(container)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
    
    def enable_pause(self):
        self.countdown_btn.setEnabled(True)

    def diable_pause(self):
        self.countdown_btn.setEnabled(False)

    def countdowner(self):
        self.experiment.countdown = not self.experiment.countdown
        if self.experiment.countdown:
            self.countdown_btn.setText("Pause")
        else:
            self.countdown_btn.setText("Resume")


    def make_info_box(self):
        font1 = QFont("Arial", 16)
        font = QFont("Arial", 20)
        font.setBold(True)

        self.info = QWidget()
        layout = QVBoxLayout(self.info)
        self.info.setStyleSheet("""
            QWidget {
                background-color: grey;
                border: 1px solid white;
                border-radius: 1px;
            }
            """)


        self.info.setFixedWidth(150)

        self.current_experiment = QLabel("None")
        self.current_experiment.setFont(font1)
        self.current_experiment.setAlignment(Qt.AlignCenter)
        self.current_experiment.setWordWrap(True)

        self.reps_count = QLabel("0/0")
        self.reps_count.setFont(font)
        self.reps_count.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.current_experiment)
        layout.addWidget(self.reps_count)
        

    def expt_start(self):
        self.logger.write_message("Experimental battery started.")
        self.experiment.start(self.graphics.fixation, self.graphics.target)
    
    def toggle_status(self):
        self.status = not self.status
        if self.status:
            self.status_box.show()
        if not self.status:
            self.status_box.hide()
    
    def update_rep_status(self, current : int, total: int):
        self.reps_count.setText(f"{current}/{total}")

    def update_exp_status(self, experiment : str):
        self.current_experiment.setText(experiment)


    def keyPressEvent(self, event):

        if event.key() == Qt.Key_E:
            self.logger.write_message("Motion artefact detected.")
            self.logger.add_event({
                "type" : "ARTEFACT"
            })

        else:
            super().keyPressEvent(event)
    
    def status_message(self, message):
        self.status_box.append(message)
