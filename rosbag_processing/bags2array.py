#!/usr/bin/python

import rosbag
import yaml
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

topic_names = ['/task_status',
                '/task_status',
                '/joy_cont',
                '/joy_cont_HA',
                '/CAinfo']

sub_topics = [['include','success','collision'],
    ]

class bagObject:
    def __init__(self,bag_name,topics, sub_topics):
        self.bag = rosbag.Bag(bag_name)
        self.topics = topics
        self.sub_topics = sub_topics

        self.get_bag_info_clean()

        for topic in topics:
            self.print_topic_example(topic)
        
        self.bag.close()


    def get_bag_info_clean(self):
        info_dict = yaml.load(self.bag._get_yaml_info())
        print("Printing information about topics with more than 1 messages")
        for item in info_dict['topics']:
            if (item['messages'] > 1): 
                print("------------")
                print("topic name: " + item['topic'] + " \t type: " + item['type'])
                print("number of messages  = " + str(item['messages']) +  " at a rate of " + str(item['frequency']) + "Hz")
        print("------------")

    def print_topic_example(self, topic_name):
        print("------------")
        print("An example message of topic: " + topic_name)
        for (topic, msg, t) in self.bag.read_messages(topics=[topic_name]):
            print(msg)
            break
        print("------------")

    # def topic_into_nparray():
    #     topic_time = 


if __name__ == '__main__':
    # + subjects[0] + '_' + interfaces[0] + '_' +
    bagname = dataroot + subjects[0] + '/bags/' + '/U00_JOY_A0_S3_2018-09-06-17-44-33.bag'
    bo = bagObject(bagname,topic_names,sub_topics)
