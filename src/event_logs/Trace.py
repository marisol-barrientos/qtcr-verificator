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

class Trace:
  def __init__(self, tr_name, events):
    self.tr_name = tr_name
    self.events = events
  
  def __repr__(self):
    res = ""
    for ev in self.events:
      res = str(res) + "\n" + str(ev)
    return res
  
  def get_conceptnames(self):
    res = []
    for ev in self.events:
      if(ev.get_conceptname() is not None):
        res.append(ev.get_conceptname())
    return res
