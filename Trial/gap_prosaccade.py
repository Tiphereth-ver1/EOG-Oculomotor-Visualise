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
        self.fixation_duration = randint(self.fixation_min,self.fixation_max)  # 《《《《《《《《《《《随机中心注视时长，毫秒，下限包含，上限不包含
        print(self.fixation_duration)
        fixation.move(0, 0)  # 《《《《《《《《《《《扫视任务中心点位置，可修改x/y坐标
        fixation.setVisible(True)
        target.setVisible(False)
        QTimer.singleShot(
            self.fixation_duration, 
            partial(
                self.begin_gap, 
                direction = DIRECTIONS[randint(0,4)],  # 《《《《《《《《《《《四方向等概率随机抽取，不保证各方向次数均衡
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
        QTimer.singleShot(self.target_duration, partial(self.clean_graphics, fixation, target))  # 《《《《《《《《《《《外围目标显示target_duration毫秒后清屏并检查下一次重复
        if (direction == Direction.LEFT):
            target.move(-self.shift,0)  # 《《《《《《《《《《《目标位于中心左侧shift，改shift调整偏移
            target.setVisible(True)
        if (direction == Direction.RIGHT):
            target.move(self.shift,0)  # 《《《《《《《《《《《目标位于中心右侧shift
            target.setVisible(True)

        if (direction == Direction.UP):
            target.move(0,-self.shift)  # 《《《《《《《《《《《目标位于中心上方shift，Qt向上为负y
            target.setVisible(True)

        if (direction == Direction.DOWN):
            target.move(0,self.shift)  # 《《《《《《《《《《《目标位于中心下方shift，Qt向下为正y
            target.setVisible(True)

        self.send_message(f"Duration: {self.fixation_duration}, Direction: {direction.value}")
        self.event_generated.emit({
            "parameters" : {
                "trial" : self.current_reps,
                "direction" : direction.value,
                "duration_ms" : self.fixation_duration
            }
        })

    
    def clean_graphics(self,
            fixation : QGraphicsEllipseItem, 
            target: QGraphicsEllipseItem, 
            ):
        target.setVisible(False)
        fixation.setVisible(False)
        self.check_repeat(fixation, target)
