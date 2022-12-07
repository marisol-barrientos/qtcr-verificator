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

import datetime

class Event:
  def __init__(self, attributes):
    self.attributes = attributes
  
  def __repr__(self):
    res = ""
    for attr in self.attributes:
      res = res + str(attr) + " | "
    return res
  
  def get_concept_name(self):
    for attr in self.attributes:
      if(attr.key == "concept:name"):
        return attr.value
    return None

  def get_activity_uuid(self):
    for uuid in self.attributes:
      if(uuid.key == 'cpee:activity_uuid'):
        return uuid.value
    return None

  def get_instance(self):
    for attr in self.attributes:
      if(attr.key == "concept:instance"):
        return attr.value
    return None

  def get_instance_id(self):
    for attr in self.attributes:
      if(attr.key == "cpee:instance"):
        return attr.value
    return None

  def get_lifecycle(self):
    for attr in self.attributes:
      if(attr.key == "lifecycle:transition"):
        return attr.value
    return None
    
  def get_timestamp(self):
    for attr in self.attributes:
      if(attr.key == "time:timestamp"):
        return datetime.datetime.strptime(attr.value, '%Y-%m-%dT%H:%M:%S.%f%z')
    return None
    
  def get_shifted_timestamp(self):
    for attr in self.attributes:
      if(attr.key == "shift:timestamp"):
        return datetime.datetime.strptime(attr.value, '%Y-%m-%dT%H:%M:%S.%f%z')
    return None
