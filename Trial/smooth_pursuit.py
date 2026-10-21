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

    def position_at(self, t):
        x, y = self.trajectory(t, self.shift, self.fz)
        return self.direction_sign * x, y

    def update_position(self):
        t = time() - self.start_time
        # print(t)
        x,y = self.position_at(t)

        self.target.move(x,y)

        if t >= self.test_duration_s:
            self.send_message("Smooth Pursuit rep finished")
            self.timer.stop()
            self.clean_graphics()
            self.event_generated.emit({
                "parameters" : {
                    "trial" : self.current_reps,
                    "initial_direction": self.initial_direction,
                    "duration_ms" : self.test_duration_s * 1000
                }
            })

    
    def run(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        self.fixation = fixation
        self.target = target
        # Alternate directions: ten repetitions give five right and five left.
        self.direction_sign = 1 if self.current_reps % 2 else -1
        self.initial_direction = "right" if self.direction_sign == 1 else "left"

        self.fixation.setVisible(False)
        x,y = self.position_at(0)

        self.target.move(x,y)

        self.target.setVisible(True)

        self.start_time = time()
        self.send_message(f"Smooth Pursuit rep started, initial direction: {self.initial_direction}")

        self.timer.start(16)  # CONFIG: Update pursuit position every 16 ms, about 62.5 times per second; actual timing depends on the event loop.


    def clean_graphics(self):
        self.phase = "rest"
        self.target.setVisible(False)
        self.fixation.setVisible(False)
        self.schedule(self.rest, partial(self.check_repeat, self.fixation, self.target))  # CONFIG: Wait rest milliseconds after each repetition, including the last, before checking completion.
