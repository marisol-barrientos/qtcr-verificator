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

import re

from src import helpers
from src.temporal_expressions import TemporalExpression


def get_temporal_expressions(text, text_name):
    temporal_expressions = []
    sentence_counter = 0
    text = helpers.remove_addition_spaces(text)
    original_sentences = helpers.get_sentences(text)
    temporally_annotated_sentences = helpers.get_temporally_annotated_sentences(text)
    for temporally_annotated_sentence in temporally_annotated_sentences:
        if "<TimeML>" in temporally_annotated_sentence:
            temporally_annotated_sentence = str(temporally_annotated_sentence.split('<TimeML>\n')[1])
        elif "</TimeML>" in temporally_annotated_sentence:
            temporally_annotated_sentence = temporally_annotated_sentence.replace("</TimeML>", "")
        number_of_temporal_expressions = int(temporally_annotated_sentence.count('TIMEX3') / 2)
        temporally_annotated_sentence = temporally_annotated_sentence.split("</TIMEX3>")
        for i in range(number_of_temporal_expressions):
            time_type_position = 3
            value_position = 5
            freq_position = 7
            quant_position = 7
            annotated_time = re.search('>(.*)</', (temporally_annotated_sentence[i] + "</TIMEX3>")).group(1)
            elements_annotated_sentence = re.split('"', temporally_annotated_sentence[i])
            temporal_expression = TemporalExpression.make_temporal_expression(
                elements_annotated_sentence[time_type_position],
                elements_annotated_sentence[value_position],
                original_sentences[sentence_counter],
                annotated_time)
            if "freq" in temporally_annotated_sentence[i]:
                temporal_expression.freq = elements_annotated_sentence[freq_position]

            if "quant" in temporally_annotated_sentence[i]:
                temporal_expression.quant = elements_annotated_sentence[quant_position]
            temporal_expression.process_description_name = text_name
            temporal_expressions.append(temporal_expression)
        sentence_counter = sentence_counter + 1

    return temporal_expressions
