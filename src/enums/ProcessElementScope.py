#
# This file is part of QTCR-VERIFICATOR.
#
# QTCR-VERIFICATOR is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# QTCR-VERIFICATOR is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with QTCR-VERIFICATOR (file COPYING in the main directory). If not, see
# http://www.gnu.org/licenses/.

from enum import Enum


# class syntax
class ProcessElementScope(Enum):
    SINGLE_ACTIVITY = 1
    ACTIVITY_SET = 2
    WHOLE_PROCESS = 3


# functional syntax
ProcessElementScope = Enum('ProcessElementScope', ['SINGLE_ACTIVITY', 'ACTIVITY_SET', 'WHOLE_PROCESS'])
