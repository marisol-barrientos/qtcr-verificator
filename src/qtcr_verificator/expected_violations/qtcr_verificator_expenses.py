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
from datetime import datetime, timedelta
import pandas as pd
import os
isp = 'Billing_Process_of_an_Internet_Service_Provider_(ISP)'
meeting = 'Meeting_Related_Activities'
quince = 'Quince_Harvesting'
expense = 'Steps_to_follow_after_receiving_Expense_Report'
all = [isp, meeting, quince, expense]
qtcr_path = '/data/input/to_evaluate/step_8/'


def get_timestamp_first_activity(df):
    concept_name = df.iloc[0]['concept:name']
    timestamps = df.loc[df['concept:name'] == concept_name]['shift:timestamp']
    desired_timestamp = datetime.strptime(timestamps.iloc[0][:19], '%Y-%m-%d %H:%M:%S')
    return desired_timestamp


def get_timestamp_last_activity(df):
    concept_name = df.iloc[len(df.index) - 1]['concept:name']
    timestamps = df.loc[df['concept:name'] == concept_name]['shift:timestamp']
    desired_timestamp = datetime.strptime(timestamps.iloc[0][:19], '%Y-%m-%d %H:%M:%S')
    return desired_timestamp


def get_duration(event_log_label, df):
    timestamps = df.loc[df['concept:name'] == event_log_label]['shift:timestamp']
    first = datetime.strptime(timestamps.iloc[0][:19], '%Y-%m-%d %H:%M:%S')
    last = datetime.strptime(timestamps.iloc[-1][:19], '%Y-%m-%d %H:%M:%S')
    return (last - first).seconds


def date_in_between(start, end, date):
    if start <= date <= end:
        return True
    else:
        return False


def read_qrtc(desired):
    all.remove(desired)
    df = pd.read_csv(qtcr_path + 'step_8.csv')
    mask = df['process_description'].isin(all)
    df = df[~mask]
    return df


def get_time(time, granularity):
    if granularity == 'MONTH':
        return datetime.strptime(time, 'XXXX-%m-%d')
    if granularity == 'HOUR':
        return datetime.strptime(time, '%H:%M:%S')
    if granularity == 'MINUTE':
        return datetime.strptime(time, '%M')
    if granularity == 'DAY':
        return datetime.strptime(time, 'XXXX-XX-%d')


def get_time_first_start(log, activity_name):
    found_activities = log.loc[log['concept:name'] == activity_name]
    found_activities = found_activities.loc[found_activities['lifecycle:transition'] == 'start']
    return datetime.strptime(
        found_activities.sort_values(by=["shift:timestamp"], ascending=True)['shift:timestamp'].iloc[0][:19],
        '%Y-%m-%d %H:%M:%S')


def get_time_last_complete(log, activity_name):
    found_activities = log.loc[log['concept:name'] == activity_name]
    found_activities = found_activities.loc[found_activities['lifecycle:transition'] == 'complete']
    return datetime.strptime(
        found_activities.sort_values(by=["shift:timestamp"], ascending=False)['shift:timestamp'].iloc[0][:19],
        '%Y-%m-%d %H:%M:%S')


# it is possible that this activity is not found because it does not exist at all, then we still check for the restriction
def is_activity_before_time(log, activity_name, status, time, granularity):
    if isinstance(time, str):
        time = get_time(time, granularity)
    found_activities = log.loc[log['concept:name'] == activity_name]
    timestamps = found_activities.loc[found_activities['lifecycle:transition'] == status]['shift:timestamp']
    for timestamp in timestamps:
        print(timestamp)
        print(time)
        timestamp = datetime.strptime(timestamp[:19], '%Y-%m-%d %H:%M:%S')
        if timestamp.day < time.day:
            return True
    return False


def before_restriction(timestamps, time_restriction):
    for timestamp in timestamps:
        timestamp = datetime.strptime(timestamp[:19], '%Y-%m-%d %H:%M:%S')
        if timestamp.day < time_restriction.day:
            return True
    return False

def after_restriction(timestamps, time_restriction):
    for timestamp in timestamps:
        timestamp = datetime.strptime(timestamp[:19], '%Y-%m-%d %H:%M:%S')
        if timestamp.day > time_restriction.day:
            return True
    return False


def in_restriction(timestamps, time_restriction):
    for timestamp in timestamps:
        timestamp = datetime.strptime(timestamp[:19], '%Y-%m-%d %H:%M:%S')
        if timestamp.day == time_restriction.day:
            return True
    return False

def in_restriction_flex(timestamps, time_restriction, flexibility):
    for timestamp in timestamps:
        timestamp = datetime.strptime(timestamp[:19], '%Y-%m-%d %H:%M:%S')
        if timestamp.day == time_restriction.day or timestamp.day == time_restriction.day  + flexibility or timestamp.day + flexibility == time_restriction.day:
            return True
    return False


def loop_logs(process_description):
    log_path = '/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/output/logs_to_csv/'+ '/' + process_description + '/'
    all_violations = []
    qrtc_file = read_qrtc(process_description)

    for filename in os.listdir(log_path):
        print(filename)
        log = pd.read_csv(log_path + filename)
        violations = verify_timestamps(qrtc_file, log, filename, process_description)
        if not violations:
            print('Any violation found\n')
        else:
            for v in violations:
                all_violations.append(v)
                print(v)
            print('\n')
    return all_violations


def verify_timestamps(qrtc_file, log, log_name, process_description):
    violations = []
    log_name = log_name[:-4]
    # iterate over qrtc requirements
    for index, row in qrtc_file.iterrows():

        qtrc_code = row['qtrc_code']
        concept_name = row['concept_name']
        activity_to = row['activity_to']
        activity_from = row['activity_from']
        #print('\nConcept Name:')
        #print(concept_name)

        timestamp_first_activity = get_timestamp_first_activity(log)
        timestamp_last_activity = get_timestamp_last_activity(log)

        status = row['status']
        granularity = row['granularity']
        reference = row['reference']
        condition = row['condition']
        reference_time = timestamp_first_activity
        reference_shift = row['reference_shift']
        condition_meet = False

        # setting reference time
        if reference != 'NO':
            reference_status = row['reference_status']
            reference_granularity = row['reference_granularity']
            if reference == 'START':
                reference_time = timestamp_first_activity + timedelta(
                    get_time(reference_shift, reference_granularity).day)
            else:
                if reference_status == 'start':
                    reference_time = get_time_first_start(log, reference)
                else:
                    reference_time = get_time_last_complete(log, reference)

        # calculating from bounder
        if activity_from == 'reference':
            activity_from = reference_time
        elif activity_from == 'shift_reference':
            activity_from = reference_time - timedelta(
                    get_time(reference_shift, reference_granularity).day)
        else:
            activity_from = get_time(activity_from, granularity)

        # calculating to bounder
        if activity_to == 'END':
            activity_to = timestamp_last_activity
        elif activity_to == 'reference':
            activity_to = reference_time
        elif activity_to == 'shift_reference':
            activity_to = reference_time - timedelta(get_time(reference_shift, reference_granularity).day)
        else:
            activity_to = get_time(activity_to, granularity)


        # in case that the qtrc bounders only the scope of the process...
        if concept_name == '*':
            if not date_in_between(activity_from, activity_to, timestamp_first_activity):
                violations.append(
                    [process_description, qtrc_code, log_name, '*', 'First activity out of range'])
            if not date_in_between(activity_from, activity_to, timestamp_last_activity):
                violations.append(
                    [process_description, qtrc_code, log_name, '*', 'Last activity out of range'])

        else:
        # if the condition is not met then we look if there is a qtcr in the consequence
            if condition != 'NO':
                condition_status = row['condition_status']
                to_condition = row['to_condition']
                condition_granularity = row['condition_granularity']
                condition_meet = is_activity_before_time(log, condition, condition_status, to_condition, condition_granularity)

            # only if the condition is not meet the consequence should happen. This path also applies for normal clauses
            if not condition_meet:
                found_activities = log.loc[log['concept:name'] == concept_name]
                to_violation = None

                    # in case that the restriction refers also to the completion of an activity
                if status == '*':
                    timestamps = found_activities.loc[found_activities['lifecycle:transition'] == 'complete'][
                        'shift:timestamp']

                    if not after_restriction(timestamps, activity_to):
                        to_violation = [process_description, qtrc_code, log_name, concept_name, 'To violated']
                        #violations.append(
                            #[process_description, qtrc_code, log_name, concept_name, 'To violated'])


                timestamps = found_activities.loc[found_activities['lifecycle:transition'] == 'start'][
                        'shift:timestamp']

                if not after_restriction(timestamps, activity_from):
                    if to_violation is not None:
                        violations.append(to_violation)
                    else:
                        violations.append(
                            [process_description, qtrc_code, log_name, concept_name, 'From violated'])

    return violations

def print_csv(violations):
    headers = ['process_description', 'QTCR_CODE', 'trace_id', 'activity_name', 'comment']
    cvs_file_name = '/data/output/to_evaluate/step_8/expected_step_8.csv'
    newfile = False
    if not os.path.exists(cvs_file_name):
        newfile = True
    with open(cvs_file_name, 'a') as fx:
        writer = csv.writer(fx)
        if newfile:
            writer.writerow(headers)
        for violation in violations:
            print(violation)
            writer.writerow(violation)


def main():
    print_csv(loop_logs(expense))


if __name__ == '__main__':
    main()
