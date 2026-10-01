from . import Trial, Direction, DIRECTIONS
from PySide6.QtWidgets import QGraphicsEllipseItem
from numpy.random import randint
from PySide6.QtCore import Qt, QTimer
from functools import partial

class Gap_Prosaccade(Trial):
    def __init__(self,
        fixation_min,
        fixation_max,
        gap,
        target_duration,
        shift,
        reps
    ):
        super().__init__() 
        self.fixation_min = fixation_min
        self.fixation_max = fixation_max
        self.gap = gap
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
        direction_choose = DIRECTIONS[randint(0,4)]
        self.send_message(f"Duration: {self.fixation_duration}, Direction: {direction_choose}")
        self.event_generated.emit({
            "parameters" : {
                "trial" : self.current_reps,
                "direction" : direction_choose,
                "duration_ms" : self.fixation_duration
            }
        })

        QTimer.singleShot(
            self.fixation_duration, 
            partial(
                self.begin_gap, 
                direction = directions_choose,
                fixation = fixation,
                target = target))
    
    def begin_gap(self, fixation, target, direction):
        fixation.setVisible(False)

        QTimer.singleShot(
            self.gap,
            partial(
                self.show_target,
                fixation,
                target,
                direction
            )
        )

    def show_target(self, 
            fixation : QGraphicsEllipseItem, 
            target: QGraphicsEllipseItem, 
            direction : Direction):
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
    
    def clean_graphics(self,
            fixation : QGraphicsEllipseItem, 
            target: QGraphicsEllipseItem, 
            ):
        target.setVisible(False)
        fixation.setVisible(False)
        self.check_repeat(fixation, target)
