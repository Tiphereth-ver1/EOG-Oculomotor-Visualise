from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QThread, Signal

from Trial import Experiment
from ui_mainwindow import Ui_MainWindow
from data_logger import Data_Logger
from Connection import Serial_Worker
from datetime import datetime

class MainWindow(QMainWindow):
    connection_request = Signal()
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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
        self.experiment.disable_pause.connect(self.disable_pause)
        self.experiment.event_sent.connect(self.logger.add_event)  # 《《《《《《《《《《《转发事件字典；日志器当前将整个字典存入type字段
        self.experiment.experiment_complete.connect(self.logger.save)

        self.setup_sidebar()

    def setup_sidebar(self):
        # Initial visibility and signal wiring belong to the controller.
        self.status_box.hide()  # 《《《《《《《《《《《Debug日志框初始隐藏

        # Connect signals
        self.expt_btn.clicked.connect(self.expt_start)  # 《《《《《《《《《《《Experiment按钮启动实验调度
        self.expt_btn.clicked.connect(self.logger.init_main_data)  # 《《《《《《《《《《《同一次点击初始化会话记录；连接顺序在启动实验槽位之后
        self.countdown_btn.clicked.connect(self.countdowner)  # 《《《《《《《《《《《Pause按钮切换倒计时，不中断刺激任务
        self.status_btn.clicked.connect(self.toggle_status)
        self.connect_btn.clicked.connect(self.connection_request.emit)
    
    def enable_pause(self):
        self.countdown_btn.setEnabled(True)

    def disable_pause(self):
        self.countdown_btn.setEnabled(False)

    def countdowner(self):
        self.experiment.countdown = not self.experiment.countdown
        if self.experiment.countdown:
            self.countdown_btn.setText("Pause")  # 《《《《《《《《《《《倒计时运行时按钮文字
        else:
            self.countdown_btn.setText("Resume")  # 《《《《《《《《《《《倒计时暂停时按钮文字


    def expt_start(self):
        self.expt_btn.setEnabled(False)
        self.logger.write_message("Experimental battery started.", self.get_time())
        self.experiment.start(self.graphics.fixation, self.graphics.target)  # 《《《《《《《《《《《将两个圆点交给实验调度器，从首块开始
    
    def toggle_status(self):
        self.status = not self.status
        if self.status:
            self.status_box.show()
        if not self.status:
            self.status_box.hide()  # 《《《《《《《《《《《Debug日志框初始隐藏
    
    def update_rep_status(self, current : int, total: int):
        self.reps_count.setText(f"{current}/{total}")

    def update_exp_status(self, experiment : str):
        self.current_experiment.setText(experiment)

    def get_time(self):
        return datetime.now().isoformat(timespec="milliseconds")

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_E:  # 《《《《《《《《《《《按E标记运动伪迹，可在此修改快捷键
            self.logger.write_message("Motion artefact detected.", self.get_time())            
            self.logger.add_event({
                "type" : "ARTEFACT"
            })

        else:
            super().keyPressEvent(event)
    
    def status_message(self, message):
        self.status_box.append(message)
