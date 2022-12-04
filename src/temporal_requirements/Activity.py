import uuid


class Activity:
    def __init__(self, name, bert_score, activity_type, signal):
        self.id = uuid.uuid4()
        self.name = name
        self.bert_score = bert_score
        self.activity_type = activity_type
        self.signal = signal
        self._status = None
        self._is_negation_clause = False

    def __repr__(self):
        return "Name: " + self.name + "\n" \
               + "BERT-SCORE: " + self.bert_score + "\n" \
               + "Activity Type: " + str(self.activity_type) + "\n" \
               + "Signal: " + str(self.signal) + "\n" \
               + "Status: " + str(self._status) + "\n" \
               + "Is Negation Clause: " + str(self._is_negation_clause)
