#!/usr/bin/python3
""" 
This is an example of how to use the csv data to make yourself a checklist
Just a linear script since it's not meant to be portable
"""


import numpy as np  

feature0 = np.genfromtxt('feature0.csv', delimiter=',')
feature1 = np.genfromtxt('feature1.csv',delimiter=',')

feature_names = [["A0 Joystick", "A1 Joystick", "A2 Joystick", "A0 Head Array", "A1 Head Array", "A2 Head Array", "A0 Sip and Puff"],
                 ["Start 1", "Start 2", "Start 3", "Start 4", "Start 5", "Start 6", "Start 7"]]


tasks = ["Door 1", "Sidewalk Wide", "Turtle Bot", "Ramp Up", "Ramp Down", "Sidewalk Narrow", "Door 2"]
num_tasks = len(tasks)

for sub_i, trials in enumerate(feature0):
    txt_str = "Subject %i \n" %sub_i
    for trial_i in range(len(trials)):
        start_pos = int(feature1[sub_i, trial_i])
        txt_str += "-----------------------------------------------------\n"
        txt_str += feature_names[0][int(feature0[sub_i, trial_i])] + "\t \t"
        txt_str += feature_names[1][start_pos] + "\n"
        txt_str += "-----------------------------------------------------\n"

        
        #cycle through the course for each starting position
        i = 0
        pos = start_pos
        while i < num_tasks:
            txt_str += tasks[pos] + "\n"
            txt_str += "-- start: \n"
            txt_str += "-- end: \n"
            txt_str += "-- collision: \n"
            txt_str += "-- other: \n"
            pos+=1
            if pos == num_tasks:
                pos = 0
            i +=1
    
    filename = "subject_%i_injured.txt" % sub_i
    f = open(filename,'w')
    f.write(txt_str)
    f.close
