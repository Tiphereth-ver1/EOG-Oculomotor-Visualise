from PySide6.QtWidgets import QMainWindow, QMessageBox, QAbstractButton
from PySide6.QtGui import QShortcut, QKeySequence
import re
from PySide6.QtCore import Qt, QThread, Signal

from Trial import Experiment
from ui_mainwindow import Ui_MainWindow
from data_logger import Data_Logger
from Connection import Serial_Worker

class MainWindow(QMainWindow):
    connection_request = Signal()
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.completed = False
        self.pause_shortcut = QShortcut(QKeySequence("Space"), self)
        self.pause_shortcut.setAutoRepeat(False)
        self.pause_shortcut.setEnabled(False)
        self.pause_shortcut.activated.connect(self.countdowner)
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
        self.experiment.pause_changed.connect(
            lambda paused: self.countdown_btn.setText("Resume" if paused else "Pause"))
        self.experiment.experiment_complete.connect(self.lock_completed_interface)
        self.experiment.event_sent.connect(self.logger.add_event)  # CONFIG: Forward the event dictionary; the logger stores it in type, except for trial pause events.
        self.experiment.experiment_complete.connect(self.logger.save)

        self.setup_sidebar()

    def setup_sidebar(self):
        # Initial visibility and signal wiring belong to the controller.
        self.status_box.hide()  # CONFIG: Hide the Debug log initially.

        # Connect signals
        self.expt_btn.clicked.connect(self.expt_start)  # CONFIG: Start experiment scheduling with the Experiment button.
        self.countdown_btn.clicked.connect(self.countdowner)  # CONFIG: Connect the Pause button to the controller pause handler.
        self.status_btn.clicked.connect(self.toggle_status)
        self.connect_btn.clicked.connect(self.connection_request.emit)
    
    def enable_pause(self):
        if self.completed:
            return
        self.countdown_btn.setEnabled(True)
        self.pause_shortcut.setEnabled(True)

    def diable_pause(self):
        self.countdown_btn.setEnabled(False)
        self.pause_shortcut.setEnabled(False)

    def countdowner(self):
        if not self.completed and self.countdown_btn.isEnabled():
            self.experiment.toggle_pause()

    def lock_completed_interface(self):
        self.completed = True
        self.pause_shortcut.setEnabled(False)
        for button in self.findChildren(QAbstractButton):
            button.setEnabled(False)
        self.subject_group.setEnabled(False)


    def expt_start(self):
        subject_id = self.subject_id_input.text().strip()
        subject_name = self.subject_name_input.text().strip()
        if not re.fullmatch(r"[A-Za-z]+(?:[ '\-][A-Za-z]+)*", subject_name):
            QMessageBox.warning(self, "Subject Name", "Enter an English name or pinyin, such as Zhang San. Spaces, hyphens, and apostrophes are allowed.")
            return
        if (not re.fullmatch(r"[A-Za-z0-9_-]+", subject_id)
                or self.age_input.value() == 0
                or self.cdr_input.currentIndex() == 0
                or self.gender_input.currentIndex() == 0):
            QMessageBox.warning(self, "Incomplete Subject Information", "Please enter age, CDR rating, and gender. Use letters, numbers, underscores, or hyphens for the subject ID, such as 01.")
            return
        subject_info = {
            "subject_id": subject_id,
            "subject_name": subject_name,
            "age": self.age_input.value(),
            "cdr": float(self.cdr_input.currentText()),
            "gender": self.gender_input.currentText(),
        }
        try:
            self.logger.init_main_data(subject_info)
        except OSError as error:
            QMessageBox.warning(self, "Unable to Create Record File", str(error))
            return
        self.subject_group.setEnabled(False)
        self.expt_btn.setEnabled(False)
        self.logger.write_message("Experimental battery started.")
        self.experiment.start(self.graphics.fixation, self.graphics.target)  # CONFIG: Pass both dots to the experiment scheduler and start with the first block.
    
    def toggle_status(self):
        self.status = not self.status
        if self.status:
            self.status_box.show()
        if not self.status:
            self.status_box.hide()  # CONFIG: Hide the Debug log initially.
    
    def update_rep_status(self, current : int, total: int):
        self.reps_count.setText(f"{current}/{total}")

    def update_exp_status(self, experiment : str):
        self.current_experiment.setText(experiment)


    def keyPressEvent(self, event):
        if self.completed:
            event.accept()
            return

        if event.key() == Qt.Key_E:  # CONFIG: Press E to mark a motion artefact; change the shortcut here.
            self.logger.write_message("Motion artefact detected.")
            self.logger.add_event({
                "type" : "ARTEFACT"
            })

        else:
            super().keyPressEvent(event)
    
    def status_message(self, message):
        self.status_box.append(message)
