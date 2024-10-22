# Imports
import re
import time
from datetime import datetime

# Constants
FILE_PATH = "./logfile.log"
BEGIN_PATTERN = r".*transaction ([0-9]+) begun$"
END_PATTERN = r".*transaction done, id=([0-9]+)$"

# Utils
def load_file(file_path):
    logs = []
    with open(file_path, 'r') as file:
        logs = file.readlines()
    return logs

def count_errors(file):
    return sum([1 for line in file if "ERROR" == line.split('\t')[1]])


def get_time_from_log_entry(line):
    return datetime.strptime(line.split('\t')[0], "%d-%m-%Y %H:%M:%S.%f")

def calc_transaction_time_ms(transaction_kvp):
    begin_time = get_time_from_log_entry(transaction_kvp[1][0])
    end_time = get_time_from_log_entry(transaction_kvp[1][1])
    return (end_time - begin_time).total_seconds() * 1000

def prepare_transaction_list(file):
    transaction_dict = dict()
    for line in file:
        match1 = re.search(BEGIN_PATTERN, line)
        if match1:
            transaction_dict[match1.group(1)] = [line.strip()]
        else:
            match2 = re.search(END_PATTERN, line)
            if match2: 
                transaction_dict[match2.group(1)].append(line.strip())
    return {k: v for k, v in transaction_dict.items() if len(v) > 1}


def calc_transaction_times(transaction_dict):
    transaction_times = []
    for transaction in transaction_dict.items():
        length = calc_transaction_time_ms(transaction)
        transaction_times.append((transaction[0], length))
    return transaction_times


def main():
    full_file = load_file(FILE_PATH)

    total_errors=count_errors(full_file)
    print(f"\nTotal numbers Error in the logfile: {total_errors}")
    transaction_dict = prepare_transaction_list(full_file)
    transaction_times =  calc_transaction_times(transaction_dict)
    print(f"\nTotal number of transactions in the logfile:{len(transaction_dict)}")
    fastest_transaction=min(transaction_times, key=lambda x: x[1])[0]
    print(f"\nThe Id of the fastest transaction in the logfile: {fastest_transaction}")
    avarage=sum(x[1] for x in transaction_times) / len(transaction_times)
    print(f"\nThe average transaction time in milliseconds: {avarage}")

main()

