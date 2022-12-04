from enum import Enum


# class syntax
class ActivityType(Enum):
    DECLARATIVE = 1
    CONDITION = 2
    CONSEQUENCE = 3
    STARTING_REFERENCE = 4


# functional syntax
ActivityType = Enum('ActivityType', ['DECLARATIVE', 'CONDITION', 'CONSEQUENCE', 'STARTING_REFERENCE'])