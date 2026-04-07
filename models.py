from enum import Enum
from datetime import datetime


class AlertLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Motion:
    timeCode = None
    alertLevel = None
    motPhoto = None

    def __init__(self, time, level, photo):
        self.timeCode = time
        self.alertLevel = level
        self.photo = photo
