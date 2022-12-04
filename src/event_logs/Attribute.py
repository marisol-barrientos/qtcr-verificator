class Attribute:
  def __init__(self, key, value):
    self.key = key
    self.value = value
  
  def __repr__(self):
    return str(self.key) + " " + str(self.value)
