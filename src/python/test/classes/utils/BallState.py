from enum import Enum


class PositionState(Enum):
    UNKNOWN = 0
    OUT = 1
    IN = 2
    NET = 3
    EDGE = 4
