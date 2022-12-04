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
