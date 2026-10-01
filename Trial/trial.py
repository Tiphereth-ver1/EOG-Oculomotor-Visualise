from abc import ABC, abstractmethod
from enum import Enum
from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtCore import QObject, Signal
from datetime import datetime

class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

DIRECTIONS = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]


# 1. Define the abstract base class
class Trial(QObject):
    finished = Signal()
    sent_message = Signal(str, str)
    update_reps = Signal(int,int)
    display_rest_timer = Signal(int)
    event_generated = Signal(dict)

    def __init__(self):
        super().__init__()
        self.reps = 3
        self.current_reps = 0
        self.rest = 0
    
    def start(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        self.current_reps = 0
        self.check_repeat(fixation, target)
        pass

    def display_rest(self, rest):
        self.display_rest_timer.emit(rest)
    
    def run(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        raise NotImplementedError
    
    def send_message(self, message : str):
        print("message emitted")
        now = datetime.now().isoformat(timespec="milliseconds")
        self.sent_message.emit(message, now)
        
    def check_repeat(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        if self.current_reps < self.reps:
            self.run(fixation, target)
            self.current_reps += 1
            print(f"Current rep: {self.current_reps}")
            self.update_reps.emit(self.current_reps, self.reps)

        elif self.current_reps == self.reps:
            self.finished.emit()
            self.update_reps.emit(self.current_reps, self.reps)

            
            


