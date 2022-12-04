from enum import Enum


# class syntax
class TimeType(Enum):
    SET = 1
    DURATION = 2
    DATE = 3
    TIME = 4


# functional syntax
TimeType = Enum('TimeType', ['SET', 'DURATION', 'DATE', 'TIME'])
