from enum import Enum


# class syntax
class ReferenceTime(Enum):
    STARTING_FIRST_ACTIVITY = 1
    ACTIVITY = 2


# functional syntax
ReferenceTime = Enum('ReferenceTime', ['STARTING_FIRST_ACTIVITY', 'ACTIVITY'])
