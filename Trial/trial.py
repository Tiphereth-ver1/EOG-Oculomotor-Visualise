from abc import ABC, abstractmethod
from enum import Enum
from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtCore import QObject, Signal


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

DIRECTIONS = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]  # 《《《《《《《《《《《可用方向；改列表长度须同步修改扫视模块randint(0,4)


# 1. Define the abstract base class
class Trial(QObject):
    finished = Signal()
    sent_message = Signal(str)
    update_reps = Signal(int,int)
    event_generated = Signal(dict)

    def __init__(self):
        super().__init__()
        self.reps = 3  # 《《《《《《《《《《《基类默认重复次数，被实验配置覆盖
        self.current_reps = 0
        self.rest = 0  # 《《《《《《《《《《《基类默认重复间休息，当前仅注视与追踪模块使用
    
    def start(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        self.current_reps = 0
        self.check_repeat(fixation, target)
        pass
    
    def run(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        raise NotImplementedError
    
    def send_message(self, message : str):
        print("message emitted")
        self.sent_message.emit(message)

        
    def check_repeat(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        if self.current_reps < self.reps:
            self.run(fixation, target)
            self.current_reps += 1
            print(f"Current rep: {self.current_reps}")
            self.update_reps.emit(self.current_reps, self.reps)

        elif self.current_reps == self.reps:
            self.finished.emit()  # 《《《《《《《《《《《重复完成后通知Experiment切换块
            self.update_reps.emit(self.current_reps, self.reps)

            
            


