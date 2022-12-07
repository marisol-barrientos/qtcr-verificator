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
import datetime
import os

from src import helpers
from src.temporal_requirements.temporal_requirements import get_temporal_requirements
from src.enums import ProcessElementScope, Conditional, Signal, ReferenceTime, TimeType, ActivityType


def get_duration(event_log_id, df):
    timestamps = df.loc[df['case:concept:name'] == event_log_id]['time:timestamp']
    first = datetime.datetime.strptime(timestamps.iloc[0], '%Y-%m-%dT%H:%M:%S.%f%z')
    last = datetime.datetime.strptime(timestamps.iloc[-1], '%Y-%m-%dT%H:%M:%S.%f%z')
    return (last - first).seconds


def write_requirements_to_csv(requirements):
    headers = ['process_description_name',
               'original_sentence',
               'annotated_time',
               'time_type',
               'value',
               'has_conditional_clause',
               'scope',
               'reference_time',
               'condition_activity',
               'consequence_activity_1',
               'consequence_activity_2',
               'reference_activity_time',
               'declarative_activity_1',
               'declarative_activity_2']

    cvs_file_name = str(helpers.to_evaluate_path) + 'extracted_requirements.csv'
    newfile = False
    if not os.path.exists(cvs_file_name):
        newfile = True
    #with open(helpers.temporal_annotations_path + 'all_extracted_temporal_expressions.csv', 'w', encoding='UTF8',
              #newline='') as fx:
    with open(cvs_file_name, 'a') as fx:
        writer = csv.writer(fx)
        if newfile:
            writer.writerow(headers)
        for requirement in requirements:
            consequence_activity_1 = True
            declarative_activity_1 = True
            row = [requirement.temporal_expression.process_description_name,
                   requirement.temporal_expression.original_sentence,
                   requirement.temporal_expression.annotated_time,
                   requirement.temporal_expression.time_type,
                   requirement.temporal_expression.value,
                   requirement.has_conditional_clause,
                   requirement.scope,
                   requirement.reference_time]

            row = row + ['NO', 'NO', 'NO', 'NO', 'NO', 'NO']
            if requirement.scope is not ProcessElementScope.ProcessElementScope.WHOLE_PROCESS:
                for activity in requirement.activities:
                    if activity.activity_type is ActivityType.ActivityType.CONDITION and consequence_activity_1:
                        row[8] = activity
                        consequence_activity_1 = False
                    elif activity.activity_type is ActivityType.ActivityType.CONDITION:
                        row[9] = activity
                    if activity.activity_type is ActivityType.ActivityType.CONSEQUENCE and declarative_activity_1:
                        row[10] = activity
                        declarative_activity_1 = False
                    elif activity.activity_type is ActivityType.ActivityType.CONSEQUENCE:
                        row[11] = activity
                        declarative_activity_1 = True
                    if activity.activity_type is ActivityType.ActivityType.STARTING_REFERENCE:
                        row[12] = activity
                    if activity.activity_type is ActivityType.ActivityType.DECLARATIVE and declarative_activity_1:
                        row[13] = activity
                    elif activity.activity_type is ActivityType.ActivityType.DECLARATIVE:
                        row[14] = activity
            writer.writerow(row)
        fx.close()


def main():
    inputs = [['Steps_to_follow_after_receiving_Expense_Report', '10db019e-7c9d-49e6-a3b5-32cdb961b93f.xes.shift.yaml.xes.shift.yaml'],
             ['Quince_Harvesting', '3db92665-7acb-4840-be68-edf258ccacfd.xes.shift.yaml.xes.shift.yaml'],
             ['Meeting_Related_Activities', '11c701ad-7bec-4181-a354-26dd3994eb82.xes.shift.yaml.xes.shift.yaml'],
            ['Billing_Process_of_an_Internet_Service_Provider_(ISP)', '1ed770da-4baa-4f06-a945-a9b06474ce3c.xes.shift.yaml.xes.shift.yaml']]
          


    input_root = '/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/input/logs/'
    out_root = '/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/input/process_descriptions/'

    for input in inputs:
        log_directory = input_root + input[0] + '/' + input[1]
        process_description_directory = out_root + input[0] + '.txt'
        requirements = get_temporal_requirements(log_directory, process_description_directory, input[0])
        for req  in requirements:
            print(req)


if __name__ == '__main__':
    main()
