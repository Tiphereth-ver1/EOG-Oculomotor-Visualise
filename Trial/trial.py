from abc import ABC, abstractmethod
from enum import Enum
from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtCore import QObject, Signal, QTimer


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

DIRECTIONS = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]  # CONFIG: Available directions; update randint(0,4) in saccade modules when changing the list length.


# 1. Define the abstract base class
class Trial(QObject):
    finished = Signal()
    sent_message = Signal(str)
    update_reps = Signal(int,int)
    event_generated = Signal(dict)

    def __init__(self):
        super().__init__()
        self.reps = 3  # CONFIG: Default repetition count in the base class; overridden by experiment configuration.
        self.current_reps = 0
        self.phase = "idle"
        self._pending = []
        self._generation = 0
        self.rest = 0  # CONFIG: Default rest between repetitions; currently used only by fixation and pursuit tasks.
    
    def start(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        self.cancel_callbacks()
        self.fixation, self.target = fixation, target
        self.current_reps = 0
        self.check_repeat(fixation, target)
        pass
    
    def run(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        raise NotImplementedError

    def schedule(self, delay, callback):
        timer = QTimer(self)
        timer.setSingleShot(True)
        generation = self._generation
        def fire():
            if generation != self._generation:
                return
            self._pending.remove((timer, callback))
            timer.timeout.disconnect()
            timer.deleteLater()
            if generation == self._generation:
                callback()
        timer.timeout.connect(fire)
        self._pending.append((timer, callback))
        timer.start(int(delay))

    def cancel_callbacks(self):
        self._generation += 1
        for timer, callback in self._pending:
            timer.stop()
            timer.timeout.disconnect()
            timer.deleteLater()
        self._pending.clear()
        if hasattr(self, "timer"):
            self.timer.stop()

    def pause(self):
        self._paused_phase = self.phase
        self._rest_callbacks = [
            (max(0, timer.remainingTime()), callback)
            for timer, callback in self._pending
        ] if self.phase == "rest" else []
        self.cancel_callbacks()
        self.phase = "paused"
        self.fixation.hide()
        self.target.hide()

    def resume(self):
        if self._paused_phase == "rest":
            self.phase = "rest"
            for delay, callback in self._rest_callbacks:
                self.schedule(delay, callback)
        else:
            self.check_repeat(self.fixation, self.target)
    
    def send_message(self, message : str):
        print("message emitted")
        self.sent_message.emit(f"{message}, trial {self.current_reps}")

        
    def check_repeat(self, fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        if self.current_reps < self.reps:
            self.current_reps += 1
            self.phase = "active"
            self.run(fixation, target)
            print(f"Current rep: {self.current_reps}")
            self.update_reps.emit(self.current_reps, self.reps)

        elif self.current_reps == self.reps:
            self.phase = "idle"
            self.update_reps.emit(self.current_reps, self.reps)
            self.finished.emit()  # Notify Experiment after the final repetition update.

            
            


