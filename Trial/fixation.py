from . import Trial, Direction, DIRECTIONS
from PySide6.QtWidgets import QGraphicsEllipseItem
from numpy.random import randint
from PySide6.QtCore import Qt, QTimer
from functools import partial
from time import time

class Fixation(Trial):
    def __init__(
        self,
        fixation_duration_s,
        reps,
        rest_duration_ms,
        rest_duration_s,
    ):
        super().__init__()

        self.fixation_duration_s = fixation_duration_s
        self.reps = reps
        self.rest_duration_ms = rest_duration_ms
        self.rest_duration_s = rest_duration_s

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_time)

        
    def check_time(self):
        t = time() - self.start_time

        if t >= self.fixation_duration_s:
            self.send_message("Fixation rep finished")
            self.timer.stop()
            self.clean_graphics()
            self.event_generated.emit({
                "parameters" : {
                    "trial" : self.current_reps,
                    "duration_ms" : self.fixation_duration_s * 1000
                }
            })

    
    def run(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        self.fixation = fixation
        self.target = target

        self.fixation.setVisible(False)
        self.target.move(0,0)
        self.target.setVisible(True)

        self.start_time = time()
        self.send_message("Fixation rep started")

        self.timer.start(1000) 


    def clean_graphics(self):
        self.target.setVisible(False)
        self.fixation.setVisible(False)
        self.display_rest(self.rest_duration_s)

        QTimer.singleShot(self.rest_duration_ms, partial(self.check_repeat, self.fixation, self.target))