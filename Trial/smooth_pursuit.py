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
    def __init__(self, trajectory):
        self.fz = 0.2
        self.test_duration_s = 5
        self.shift = 400
        self.trajectory = trajectory
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
    
    def set_trajectory(self, trajectory):
        self.trajectory = trajectory

    def update_position(self):
        t = time() - self.start_time
        print(t)
        x,y = self.trajectory(t, self.shift, self.fz)

        self.target.move(x,y)

        if t >= self.test_duration_s:
            print("test is done")
            self.timer.stop()
            self.clean_graphics()
    
    def run(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        self.fixation = fixation
        self.target = target

        self.fixation.setVisible(False)
        x,y = self.trajectory(0, self.shift, self.fz)

        self.target.move(x,y)

        self.target.setVisible(True)

        self.start_time = time()
        print("test is started")

        self.timer.start(16) 


    def clean_graphics(self):
        self.target.setVisible(False)
        self.fixation.setVisible(False)
