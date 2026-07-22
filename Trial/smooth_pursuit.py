from . import Trial, Direction, DIRECTIONS
from PySide6.QtWidgets import QGraphicsEllipseItem
from numpy.random import randint
from PySide6.QtCore import Qt, QTimer
from functools import partial
from numpy import sin, pi
from time import time
from .trajectories import (
    circle,
    figure8,
    horizontal_sinusoid,
)

class Smooth_Pursuit(Trial):
    def __init__(self, 
        fz,
        test_duration_s,
        shift,
        trajectory,
        reps,
        rest
    ):
        super().__init__() 
        self.fz = fz
        self.test_duration_s = test_duration_s
        self.shift = shift
        self.trajectory = trajectory
        self.reps = reps
        self.rest = rest

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
    
    def set_trajectory(self, trajectory):
        self.trajectory = trajectory

    def update_position(self):
        t = time() - self.start_time
        # print(t)
        x,y = self.trajectory(t, self.shift, self.fz)

        self.target.move(x,y)

        if t >= self.test_duration_s:
            self.send_message("Smooth Pursuit rep finished")
            self.timer.stop()
            self.clean_graphics()
            self.event_generated.emit({
                "parameters" : {
                    "trial" : self.current_reps,
                    "duration_ms" : self.test_duration_s * 1000
                }
            })

    
    def run(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        self.fixation = fixation
        self.target = target

        self.fixation.setVisible(False)
        x,y = self.trajectory(0, self.shift, self.fz)

        self.target.move(x,y)

        self.target.setVisible(True)

        self.start_time = time()
        self.send_message("Smooth Pursuit rep started")

        self.timer.start(16) 


    def clean_graphics(self):
        self.target.setVisible(False)
        self.fixation.setVisible(False)
        QTimer.singleShot(self.rest, partial(self.check_repeat, self.fixation, self.target))