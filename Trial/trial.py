from abc import ABC, abstractmethod
from enum import Enum
from PySide6.QtWidgets import QGraphicsEllipseItem

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

DIRECTIONS = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]


# 1. Define the abstract base class
class Trial(ABC):
    
    @abstractmethod
    def run(fixation : QGraphicsEllipseItem, target: QGraphicsEllipseItem):
        """Each processor needs api keys configured."""
        pass

    # @abstractmethod
    # def stop(self, amount: float):
    #     """Each processor must implement a charge behavior."""
    #     pass
        
    # def reset(self, amount: float):
    #     """Concrete method: Shared behavior inherited by all subclasses."""
    #     print(f"Receipt generated for ${amount}")

