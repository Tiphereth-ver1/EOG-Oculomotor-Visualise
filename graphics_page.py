from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)
from PySide6.QtGui import QBrush
from PySide6.QtCore import Qt, QTimer
from functools import partial
from Trial import Step_Prosaccade, Gap_Prosaccade, Overlap_Prosaccade, Smooth_Pursuit
from Trial.trajectories import (
    circle,
    figure8,
    horizontal_sinusoid,
)


from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QBrush
from PySide6.QtCore import Qt
from numpy.random import randint

from enum import Enum

radius = 24
centre = round(radius/2)
SHIFT = 400

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Stimulus(QGraphicsEllipseItem):
    def __init__(self, color):
        super().__init__(
            -radius/2,
            -radius/2,
            radius,
            radius
        )        
        self.setBrush(QBrush(color))

    def move(self, x, y):
        self.setPos(x, y)

    def hide(self):
        self.hide()

    def show(self):
        self.show()


class Graphics_Page(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.graphics_scene = QGraphicsScene(self)
        self.graphics_scene.setSceneRect(-600, -350, 1200, 700)
        self.centerOn(0, 0)
        self.setScene(self.graphics_scene)

        self.step_prosaccade = Step_Prosaccade()
        self.gap_prosaccade = Gap_Prosaccade()
        self.overlap_prosaccade = Overlap_Prosaccade()
        self.smooth_pursuit = Smooth_Pursuit(figure8)

        self.fixation = Stimulus(Qt.GlobalColor.blue)
        self.target = Stimulus(Qt.GlobalColor.white)
        self.graphics_scene.addItem(self.fixation)
        self.graphics_scene.addItem(self.target)
        self.directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
    
    def move_dot(self):
        self.fixation.move(randint(-500,500), randint(-500,500))
        self.target.move(randint(-500,500), randint(-500,500))
    
    def step_prosaccade_run(self):
        self.step_prosaccade.run(self.fixation, self.target)
    
    def gap_prosaccade_run(self):
        self.gap_prosaccade.run(self.fixation, self.target)

    def overlap_prosaccade_run(self):
        self.overlap_prosaccade.run(self.fixation, self.target)

    def smooth_pursuit_circle_run(self):
        self.smooth_pursuit.set_trajectory(circle)
        self.smooth_pursuit.run(self.fixation, self.target)

    def smooth_pursuit_figure8_run(self):
        self.smooth_pursuit.set_trajectory(figure8)
        self.smooth_pursuit.run(self.fixation, self.target)

    def smooth_pursuit_horizontal_run(self):
        self.smooth_pursuit.set_trajectory(horizontal_sinusoid)
        self.smooth_pursuit.run(self.fixation, self.target)
    # def setup_prosaccade(self):
    #     fixation_duration = randint(1000,1500)
    #     print(fixation_duration)
    #     target_duration = 1000
    #     self.fixation.setVisible(True)
    #     self.target.setVisible(False)
    #     self.fixation.move(0, 0)
    #     QTimer.singleShot(
    #         fixation_duration, 
    #         partial(
    #             self.step_prosaccade, 
    #             direction = self.directions[randint(0,4)]))

    # def step_prosaccade(self, direction : Direction):
    #     target_duration = 1000
    #     self.fixation.setVisible(False)
    #     QTimer.singleShot(target_duration, self.clean_graphics)
    #     if (direction == Direction.LEFT):
    #         self.target.move(-SHIFT,0)
    #         self.target.setVisible(True)
    #     if (direction == Direction.RIGHT):
    #         self.target.move(SHIFT,0)
    #         self.target.setVisible(True)

    #     if (direction == Direction.UP):
    #         self.target.move(0,SHIFT)
    #         self.target.setVisible(True)

    #     if (direction == Direction.DOWN):
    #         self.target.move(0,-SHIFT)
    #         self.target.setVisible(True)

    # def clean_graphics(self):
    #     self.target.setVisible(False)
    #     self.fixation.setVisible(False)
