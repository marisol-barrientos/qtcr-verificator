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

import csv
import os
import helpers
from src.temporal_expressions.temporal_expressions import get_temporal_expressions


def write_to_individual_txt():
    files = os.listdir(helpers.process_description_path)
    extracted_temporal_expressions = []
    for file in files:
        if os.path.isfile(os.path.join(helpers.process_description_path, file)):
            f = open(os.path.join(helpers.process_description_path, file), 'r')
            extracted_temporal_expressions.append(
                [helpers.temporal_expressions_path + file[:-4] + '.txt', get_temporal_expressions(
                    helpers.get_all_sentences(f), file[:-4] + '.txt')])

    for temporal_expression in extracted_temporal_expressions:
        file_name = ''.join(map(str, temporal_expression[0]))
        temporal_expression = ''.join(map(str, temporal_expression[1]))
        helpers.create_annotated_file(file_name, temporal_expression)
        f.close()


def write_to_unique_csv():
    files = os.listdir(helpers.process_description_path)
    files_extracted_temporal_expressions = []
    for file in files:
        if os.path.isfile(os.path.join(helpers.process_description_path, file)):
            f = open(os.path.join(helpers.process_description_path, file), 'r')
            files_extracted_temporal_expressions.append(get_temporal_expressions(helpers.get_all_sentences(f), file[:-4] + '.txt'))

    headers = ['process_description_name', 'original_sentence', 'annotated_time', 'time_type', 'value', 'quantity',
               'frequency']

    with open(helpers.to_evaluate_path + 'extracted_temporal_expressions.csv', 'w', encoding='UTF8', newline='') as fx:
        writer = csv.writer(fx)
        writer.writerow(headers)
        for file_extracted_temporal_expressions in files_extracted_temporal_expressions:
            for temporal_expression in file_extracted_temporal_expressions:
                row = [temporal_expression.process_description_name[:-4],
                       temporal_expression.original_sentence,
                       temporal_expression.annotated_time,
                       temporal_expression.time_type,
                       temporal_expression.value]
                if temporal_expression.quant:
                    row.append(temporal_expression.quant)
                else:
                    row.append("")
                if temporal_expression.freq:
                    row.append(temporal_expression.freq)
                writer.writerow(row)
        fx.close()


def main():
    write_to_unique_csv()


if __name__ == '__main__':
    main()
