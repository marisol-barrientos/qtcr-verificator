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
