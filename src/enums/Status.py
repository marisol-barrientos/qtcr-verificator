from enum import Enum


# class syntax
class Status(Enum):
    START = 1
    COMPLETE = 2


# functional syntax
Status = Enum('Status', ['START', 'COMPLETE'])
