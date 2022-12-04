from enum import Enum


# class syntax
class ProcessElementScope(Enum):
    SINGLE_ACTIVITY = 1
    ACTIVITY_SET = 2
    WHOLE_PROCESS = 3


# functional syntax
ProcessElementScope = Enum('ProcessElementScope', ['SINGLE_ACTIVITY', 'ACTIVITY_SET', 'WHOLE_PROCESS'])
