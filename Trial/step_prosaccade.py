from . import Trial, Direction, DIRECTIONS
from PySide6.QtWidgets import QGraphicsEllipseItem
from numpy.random import randint
from PySide6.QtCore import Qt, QTimer
from functools import partial

class Step_Prosaccade(Trial):
    def __init__(
        self,
        fixation_min,
        fixation_max,
        target_duration,
        shift,
        reps
    ):
        super().__init__()

        self.fixation_min = fixation_min
        self.fixation_max = fixation_max
        self.target_duration = target_duration
        self.shift = shift
        self.reps = reps
        self.fixation_duration = 0
        
    def run(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        self.fixation_duration = randint(self.fixation_min,self.fixation_max)
        print(self.fixation_duration)
        fixation.move(0, 0)
        fixation.setVisible(True)
        target.setVisible(False)
        QTimer.singleShot(
            self.fixation_duration, 
            partial(
                self.step_prosaccade, 
                direction = DIRECTIONS[randint(0,4)],
                fixation = fixation,
                target = target))

    def step_prosaccade(self, 
            fixation : QGraphicsEllipseItem, 
            target: QGraphicsEllipseItem, 
            direction : Direction):
        fixation.setVisible(False)
        QTimer.singleShot(self.target_duration, partial(self.clean_graphics, fixation, target))
        if (direction == Direction.LEFT):
            target.move(-self.shift,0)
            target.setVisible(True)
        if (direction == Direction.RIGHT):
            target.move(self.shift,0)
            target.setVisible(True)

        if (direction == Direction.UP):
            target.move(0,-self.shift)
            target.setVisible(True)

        if (direction == Direction.DOWN):
            target.move(0,self.shift)
            target.setVisible(True)
        
        self.send_message(f"Duration: {self.fixation_duration}, Direction: {direction.value}")

    def clean_graphics(self,
            fixation : QGraphicsEllipseItem, 
            target: QGraphicsEllipseItem, 
            ):
        target.setVisible(False)
        fixation.setVisible(False)
        self.check_repeat(fixation, target)
