#!/usr/bin/python3
import csv
import numpy as np
import random
from active_balance_functions import *

#TODO make this an argument
active_balance_file_path = '/mnt/NUdata/2018-Adaptive-Autonomy-Wheelchair/data/balanced_tasks/injured/sci/live_sci_balancing.csv'

balance_targets = ['interface', 'assistance', 'start']
balance_counts = [3,3,7]


#initialize
csv_dict = {}
balance_dict = {}
csv_dict['raw'] = []
completion = []
for t_i, target in enumerate(balance_targets):
    csv_dict[target] = []
    if target == 'assistance':
        balance_dict[target+'_joy'] = np.zeros((balance_counts[t_i], balance_counts[t_i]))
        balance_dict[target+'_ha'] = np.zeros((balance_counts[t_i], balance_counts[t_i]))
    else:
        balance_dict[target] = np.zeros((balance_counts[t_i],balance_counts[t_i]))


#grab csv and sort into dict
with open(active_balance_file_path,newline='') as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    for row in reader:
        csv_dict['raw'].append(row)
        if row[1] in balance_targets:
            csv_dict[row[1]].append(row[2:])
        elif row[1] == 'completed':
            completion.append(row[2:])

# TODO add checks for size of all dicts to ensure they match

print(completion)
#the rows (first index) are the balance target and columns are position

# get counts

### interface and assistance balancing (checked this by hand, should be correct)
for row_i, row in enumerate(csv_dict['interface']):
    pos = 0
    looking_for_joy = True
    looking_for_ha = True
    for t_i, trial in enumerate(row):
        if completion[row_i][t_i] == 'n':
            print("not completed so skipping")
            continue

        if trial == 'joy' and looking_for_joy:
            balance_dict['interface'][0,pos] += 1 
            pos += 1
            looking_for_joy = False 
            for i in range(3):
                balance_dict['assistance_joy'][int(csv_dict['assistance'][row_i][t_i+i]), i] += 1
        
                
        elif trial == 'ha' and looking_for_ha:
            balance_dict['interface'][1, pos] += 1
            pos += 1
            looking_for_ha = False
            for i in range(3):
                balance_dict['assistance_ha'][int(csv_dict['assistance'][row_i][t_i+i]), i] += 1
        elif trial == 'snp':
            balance_dict['interface'][2, pos] += 1
            pos += 1

        # else: #use this if the 
        #     balance_dict[target][]

print(csv_dict['start'])
# get start count
for row_i, row in enumerate(csv_dict['start']):
    pos = 0
    for t_i, start in enumerate(row):
        if completion[row_i][t_i] == 'n':
            print("not completed so skipping")
            continue
        balance_dict['start'][int(start)-1,pos] += 1
        pos+= 1


        

print("interface array",balance_dict['interface'])
fo = get_next_balance(balance_dict['interface'])

print(fo)
