#!/usr/bin/python3

"""
this is a script....


The count arrays through out indicate how many times a feature (row)
    has appeared in a certain position column

for example:
    [[1 2 3],
    [2 1 3],
    [1 1 1]]

    translates to: 
    feature 0 has appeared 1 time in the first positon, 2 in 2nd, and 3 in 3rd
    feature 1 has appeared 2 times in first position, 1 in 2nd, and 3 in 3rd
    feature 2 has appeared 1 time in all positions

This script rebalances and prioritizes the first features
"""
import csv
import numpy as np
import random
from active_balance_functions import *
from print_checklist_functions import *
#TODO make this an argument

## tunable parameters
active_balance_file_path = '/mnt/NUdata/2018-Adaptive-Autonomy-Wheelchair/data/balanced_tasks/injured/sci/'
subject = 9

### constants used for balancing ###
balance_targets = ['interface', 'assistance', 'start']
balance_counts = [3,3,7]

### constants for printing ####
feature_names = [["Joystick", "Head Array", "Sip and Puff"],
                 ["A0", "A1", "A2"],
                 ["Start 1", "Start 2", "Start 3", "Start 4", "Start 5", "Start 6", "Start 7"]]


tasks = ["Door 1", "Sidewalk Wide", "Turtle Bot",
         "Ramp Up", "Ramp Down", "Sidewalk Narrow", "Door 2"]

#items I want to check off each tasks 
notes = ["start", "end", "collision", "other"]


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
with open(active_balance_file_path+'live_sci_balancing.csv', newline='') as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    for row in reader:
        csv_dict['raw'].append(row)
        if row[1] in balance_targets:
            csv_dict[row[1]].append(row[2:])
        elif row[1] == 'completed':
            completion.append(row[2:])

# TODO add checks for size of all dicts to ensure they match

### interface and assistance balancing (checked this by hand, should be correct)
for row_i, row in enumerate(csv_dict['interface']):
    pos = 0
    looking_for_joy = True
    looking_for_ha = True
    for t_i, trial in enumerate(row):
        if completion[row_i][t_i] == 'n':
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

# get start count (Checked by hand, should be correct)
for row_i, row in enumerate(csv_dict['start']):
    pos = 0
    for t_i, start in enumerate(row):
        if completion[row_i][t_i] == 'n':
            continue
        balance_dict['start'][int(start)-1,pos] += 1
        pos+= 1

order_dict = {}
orders = ['interface','assistance_joy','assistance_ha','start']
for order in orders:
    # print(order, balance_dict[order])
    order_dict[order] = balance_first_pos_priority(balance_dict[order])

    print(order, order_dict[order])

assistance_levels = [order_dict['assistance_joy'],order_dict['assistance_ha'],[0]] 

####################
# Check that the results make sense
################
for order in orders:
    print("---------------------------------")
    print("order for", order, ":\n",order_dict[order])
    print("previous balance of", order, ":\n", balance_dict[order])
    for pos, feature in enumerate(order_dict[order]):
        balance_dict[order][feature,pos] += 1
    print("new balance of", order, ":\n", balance_dict[order])


###############
# PRINT RESULTS TO TXT
#############
num_tasks = len(tasks)

start_count = 0
txt_str = "Subject %i \n" % subject
for trial_i, interface_num in enumerate(order_dict['interface']):

    assist_levels_in_interface = assistance_levels[
        interface_num]
    for assist_level in assist_levels_in_interface:
        start_pos = int(order_dict['start'][start_count])
        start_count += 1
        tags = [feature_names[0][int(interface_num)],
                feature_names[1][int(assist_level)],
                feature_names[2][start_pos]]
        txt_str += print_trial_header(tags)
        txt_str += "MC10: \n"

        #cycle through the course for each starting position
        i = 0
        pos = start_pos
        while i < num_tasks:
            txt_str += print_event(tasks[pos],notes)
            pos += 1
            if pos == num_tasks:
                pos = 0
            i += 1

            txt_str += "MC10: \n"
filename = "subject_%i_sci.txt" % (subject)
print("Printing to file.... ", filename)
print("the location of the file is: ", active_balance_file_path)
f = open(active_balance_file_path +  filename, 'w')
f.write(txt_str)
f.close


