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

from src.temporal_requirements.temporal_requirements import get_temporal_requirements


def main():
    isp = 'Billing_Process_of_an_Internet_Service_Provider_(ISP)'
    meeting = 'Meeting_Related_Activities'
    quince = 'Quince_Harvesting'
    expense = 'Steps_to_follow_after_receiving_Expense_Report'
    input_root = '/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/input/logs/'
    output_root = '/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/output/logs_to_csv/'

    log_path = '/event_logs/383c2ed9-8787-4756-9e24-cb44a14841ac.xes.shift.yaml'
    process_description_path = '/data/input/process_descriptions/Quince_Harvest.txt'
    print(get_temporal_requirements(log_path, process_description_path, isp))


if __name__ == '__main__':
    main()
