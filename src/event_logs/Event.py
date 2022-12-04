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
