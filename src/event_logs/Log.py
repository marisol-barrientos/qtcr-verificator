import csv
from src.event_logs.Attribute import Attribute
from src.event_logs.Event import Event
from src.event_logs.Trace import Trace
from pathlib import PurePath
import yaml


class Log:
    def __init__(self, input_path, filename):
        self.input_path = input_path
        self.filename = filename
        self.output_name = filename.replace('.xes', '')
        self.traces = []
        self.events = []

    def __repr__(self):
        res = ""
        for tr in self.traces:
            res = res + str(tr) + "\n\n"
        return res

    def parse_csv(self):
        with open(PurePath(str(self.input_path)).joinpath(str(self.filename))) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tr_name = None
                attributes = list()
                for k, v in row.items():
                    if (k == "case:concept:name" and (tr_name == None or tr_name != v)):
                        self.events.clear()
                        tr_name = v
                    if (k != "case:concept:name"):
                        attributes.append(Attribute(k, v))
                    self.events.append(Event(attributes))
                self.traces.append(Trace(tr_name, self.events))

    def set_traces_and_events(self):
        stream = open(PurePath(str(self.input_path)).joinpath(str(self.filename)), 'r')
        docs = yaml.load_all(stream, yaml.FullLoader)
        tr_name = None
        for doc in docs:
            for k, v in doc.items():
                attributes = list()
                if ("cpee:lifecycle:transition" in v.keys() and (
                        "activity/done" in v.values() or "activity/calling" in v.values())):
                    for k2, v2 in v.items():
                        attributes.append(Attribute(k2, v2))
                    self.events.append(Event(attributes))
                    #print(attributes)
                    tr_name = v["cpee:instance"]
                    #print(tr_name)
            self.traces.append(Trace(tr_name, self.events))
