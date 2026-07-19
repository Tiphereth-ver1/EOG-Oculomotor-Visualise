from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsTextItem, QSizePolicy)
from PySide6.QtGui import QBrush, QFont, QTextCursor, QTextBlockFormat
from PySide6.QtCore import Qt, QTimer
from functools import partial
from Trial import Experiment
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

# class Direction(Enum):
#     LEFT = "Left"
#     RIGHT = "Right"
#     UP = "Up"
#     DOWN = "Down"

title_font = QFont("Arial", 32)
title_font.setBold(True)

instructions_font = QFont("Arial", 20)


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

class Graphics_Page(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.graphics_scene = QGraphicsScene(self)
        self.graphics_scene.setSceneRect(-600, -350, 1200, 700)
        self.centerOn(0, 0)
        self.setScene(self.graphics_scene)

        self.fixation = Stimulus(Qt.GlobalColor.yellow)
        self.target = Stimulus(Qt.GlobalColor.white)

        self.title = QGraphicsTextItem("")
        self.title.setFont(title_font)

        self.instructions = QGraphicsTextItem("")
        self.instructions.setFont(instructions_font)
        self.instructions.setTextWidth(700)

        self.graphics_scene.addItem(self.fixation)
        self.fixation.hide()

        self.graphics_scene.addItem(self.target)
        self.target.hide()

        self.graphics_scene.addItem(self.instructions)
        self.graphics_scene.addItem(self.title)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        
    def show_title(self, text):
        self.instructions.hide()

        self.title.setPlainText(text)

        rect = self.title.boundingRect()
        self.title.setPos(
            -rect.width() / 2,
            -rect.height() / 2
        )

        self.title.show()    

    def show_instruction(self, text):
        self.title.hide()

        self.instructions.setPlainText(text)

        cursor = self.instructions.textCursor()
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cursor.select(QTextCursor.SelectionType.Document)
        cursor.mergeBlockFormat(block_format)

        self.instructions.setTextCursor(cursor)

        rect = self.instructions.boundingRect()
        self.instructions.setPos(
            -rect.width() / 2,
            -rect.height() / 2
        )

        self.instructions.show()

    def clear_text(self):
        self.title.hide()
        self.instructions.hide()