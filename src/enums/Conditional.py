from enum import Enum


# class syntax
class Conditional(Enum):
    IF = 1
    OTHERWISE = 2
    NONE = 3


# functional syntax
Conditional = Enum('Conditional', ['IF', 'OTHERWISE', 'NONE'])
