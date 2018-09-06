#!/usr/bin/python

import rosbag
import numpy as np
#################################################
##### TUNABLE PARAMETERs #######################
#################################################
mnt_folder = '/mnt/NUdata/'
subjects = ['U00']
interfaces = ['JOY', 'HA','SNP']
assistance_levels = ['A0','A1','A2']

output_folder = 'nparrays'





dataroot = mnt_folder + '2018-Adaptive-Autonomy-Wheelchair/data/study/'

topic_names = ['task_status',
                'task_status',
                'joy_cont',
                'joy_cont_HA',
                'CA_info']

sub_topics = [['include','success','collision'],
    ]



if __name__ == '__main__':
    # + subjects[0] + '_' + interfaces[0] + '_' +
    bagname = dataroot + subjects[0] + '/bags/' + 'U00_JOY_A0_S4_2018-09-05-16-27-43.bag'
    #for everytopic, grab the header info
    bag = rosbag.Bag(bagname)
    # for thing in bag.get_type_and_topic_info():
    #     print(thing)
    array_init = False
    for (topic, msg, t) in bag.read_messages(topics=['/task_status']):
        t = msg.header.stamp.sec + msg.header.stamp.nsecs/1e9
        header_info_array = np.array([t, msg.header.frame_id])
        data_array = np.array([getattr(msg,sub_topics[0][0])])

        #if (!array_init):
            
        print(topic, msg.header.stamp.nsecs/1e9)
        #np.a

    bag.close()
