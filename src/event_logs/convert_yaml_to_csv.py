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

from src.event_logs.Log import Log


def main():
    isp = 'Billing_Process_of_an_Internet_Service_Provider_(ISP)'
    meeting = 'Meeting_Related_Activities'
    quince = 'Quince_Harvesting'
    expense = 'Steps_to_follow_after_receiving_Expense_Report'
    input_root = '/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/input/logs/'
    output_root = '/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/output/logs_to_csv/'

    input = input_root + quince + '/'
    output = output_root + quince + '/'

    for file in os.listdir(input):
        file_directory = input + file
        log = Log('', file_directory)
        log.set_traces_and_events()
        headers = ['cpee:activity_uuid', 'concept:name', 'lifecycle:transition', 'shift:timestamp']
        new_file_name = file.replace('.xes.shift.yaml.xes.shift.yaml', '') + '.csv'
        with open(output + new_file_name,
                  'w', encoding='UTF8', newline='') as fx:
            writer = csv.writer(fx)
            writer.writerow(headers)
            for event in log.events:
                writer.writerow([str(event.get_activity_uuid()),
                                 str(event.get_concept_name()),
                                 str(event.get_lifecycle()),
                                 str(event.get_shifted_timestamp())])
            fx.close()


if __name__ == '__main__':
    main()
