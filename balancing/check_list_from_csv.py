#!/usr/bin/python3
""" 
This is an example of how to use the csv data to make yourself a checklist
Just a linear script since it's not meant to be portable
"""


import numpy as np  

subject_groups = ['ui','sci','als','cp']
interface_names = ['joy','ha']
for sub_group in subject_groups:
    feature0 = np.genfromtxt(sub_group+'_interface_balance.csv', delimiter=',')
    joy_assistance_levels = np.genfromtxt(sub_group + '_joy_balance.csv', delimiter=',')
    ha_assistance_levels = np.genfromtxt(sub_group + '_ha_balance.csv', delimiter=',')
    assistance_levels = [joy_assistance_levels, ha_assistance_levels, np.zeros([len(joy_assistance_levels[:,0]), 1])]

    start_positions = np.genfromtxt(sub_group+'_start_balance.csv', delimiter=',')
    feature_names = [["Joystick", "Head Array", "Sip and Puff"],
                     ["A0", "A1", "A2"],
                     ["Start 1", "Start 2", "Start 3", "Start 4", "Start 5", "Start 6", "Start 7"]]

    # feature_names = [["A0 Joystick", "A1 Joystick", "A2 Joystick", "A0 Head Array", "A1 Head Array", "A2 Head Array", "A0 Sip and Puff"],
    #                 ["Start 1", "Start 2", "Start 3", "Start 4", "Start 5", "Start 6", "Start 7"]]


    tasks = ["Door 1", "Sidewalk Wide", "Turtle Bot", "Ramp Up", "Ramp Down", "Sidewalk Narrow", "Door 2"]
    num_tasks = len(tasks)

    
    for sub_i, trials in enumerate(feature0):
        start_count = 0
        txt_str = "Subject %i \n" %sub_i
        for trial_i, interface_num in enumerate(trials):
            
            assist_levels_in_interface = assistance_levels[trial_i][sub_i]
            #print(assistance_levels)
            for assist_level in assist_levels_in_interface:
                print(start_count)
                start_pos = int(start_positions[sub_i, start_count])
                start_count += 1
                txt_str += "-----------------------------------------------------\n"
                txt_str += feature_names[0][int(interface_num)] + "\t "
                txt_str += feature_names[1][int(assist_level)] + "\t "
                #txt_str += feature_names[0][int(feature0[sub_i, trial_i])] + "\t \t"
                txt_str += feature_names[2][start_pos] + "\n"
                txt_str += "-----------------------------------------------------\n"
                txt_str += "MC10: \n"

                #cycle through the course for each starting position
                i = 0
                pos = start_pos
                while i < num_tasks:
                    txt_str += tasks[pos] + "\n"
                    txt_str += "-- start: \n"
                    txt_str += "-- end: \n"
                    txt_str += "-- collision: \n"
                    txt_str += "-- other: \n"
                    pos += 1
                    if pos == num_tasks:
                        pos = 0
                    i += 1

                txt_str += "MC10: \n"
        filename = "subject_%i_%s.txt" % (sub_i, sub_group)
        f = open(filename,'w')
        f.write(txt_str)
        f.close
