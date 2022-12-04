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
