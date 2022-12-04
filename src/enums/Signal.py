from enum import Enum


# class syntax
class Signal(Enum):
    IN = 1
    BEFORE = 2
    AFTER = 3
    EACH = 4


# functional syntax
Signal = Enum('Signal', ['IN', 'BEFORE', 'AFTER', 'EACH'])
