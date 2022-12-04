import csv
import os

import pandas as pd

isp = 'Billing_Process_of_an_Internet_Service_Provider_(ISP)'
meeting = 'Meeting_Related_Activities'
quince = 'Quince_Harvesting'
expense = 'Steps_to_follow_after_receiving_Expense_Report'
all = [isp, meeting, quince, expense]


def read_expected_qtcr_violations():
    df = pd.read_csv('/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/output/to_evaluate/step_8/expected_step_8_v1.csv')
    return df


def read_extracted_qtcr_violations():
    df = pd.read_csv('/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/output/to_evaluate/step_8/qtcr_auto_step_8_v1.csv')
    return df

def read_file_with_ids():
    df = pd.read_csv('/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/output/to_evaluate/step_8/calculate_TN.csv')
    return df



def find_qtcr_code_trace_id(df, to_find):
    return df.loc[df['trace_id'] == to_find]['QTCR_CODE'].values

def not_found_qtcr_code_trace_id(df, to_find):
    return df.loc[df['trace_id'] != to_find]['QTCR_CODE'].values



def write_to_csv_log_ids(process_description):
    headers = ['trace_id']
    csv_file_name = '/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/output/to_evaluate/step_8/' + process_description + '.csv'
    log_path = '/home/marisolbarrientosmoreno/Desktop/Summer_Semester/i17/deadline/regulatory-documents-tie/temporal_compliance_verificator/data/output/logs_to_csv/' + '/' + process_description + '/'
    newfile = False
    if not os.path.exists(csv_file_name):
        newfile = True
    with open(csv_file_name, 'a') as fx:
        writer = csv.writer(fx)
        if newfile:
            writer.writerow(headers)
        for filename in os.listdir(log_path):
            filename = filename[:-4]
            writer.writerow([filename])

def filter_by_process_description(df, desired):
    all.remove(desired)
    mask = df['process_description'].isin(all)
    all.append(desired)
    return df[~mask]


def extract_measures(process_description):
    TP = 0
    FN = 0
    FP = 0

    expected_qtcr_violations = read_expected_qtcr_violations()
    extracted_qtcr_violations = read_extracted_qtcr_violations()

    if process_description != 'all':
        expected_qtcr_violations = filter_by_process_description(expected_qtcr_violations, process_description)
        extracted_qtcr_violations = filter_by_process_description(extracted_qtcr_violations, process_description)

    for index, row in expected_qtcr_violations.iterrows():
        trace_id = row['trace_id']
        if trace_id in extracted_qtcr_violations.values:
            TP = TP + 1
        else:
            FN = FN + 1

    for index, row in extracted_qtcr_violations.iterrows():
        trace_id = row['trace_id']
        if trace_id not in expected_qtcr_violations.values:
            FP = FP + 1

    return TP, FN, FP


def main():
    print(quince + ': ' + str(extract_measures(quince)))
    print(isp + ': ' + str(extract_measures(isp)))
    print(meeting + ': ' + str(extract_measures(meeting)))
    print(expense + ': ' + str(extract_measures(expense)))
    print('All together: ' + str(extract_measures('all')))


if __name__ == '__main__':
    main()
