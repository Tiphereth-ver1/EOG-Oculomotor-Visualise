from abc import ABC, abstractmethod
from enum import Enum
from PySide6.QtWidgets import QGraphicsEllipseItem

class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

DIRECTIONS = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]


# 1. Define the abstract base class
class Trial(ABC):
    def __init__(self):
        self.reps = 3
        self.current_reps = 0
        self.rest = 0
    
    def start(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        self.current_reps = self.reps
        self.run(fixation, target)
        pass
    
    @abstractmethod
    def run(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        """Run the trial for the target."""
        pass

        
    def check_repeat(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        print(f"Current rep: {self.current_reps}")
        if self.current_reps > 0:
            self.run(fixation, target)
            self.current_reps-=1
            


