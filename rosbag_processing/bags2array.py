#!/usr/bin/python

import rosbag
import yaml
import numpy as np
import operator      #makes it easier to pull sub-topics using attrgetter


class bagObject:
    def __init__(self,bag_name,topics, subtopics,save_prefix):
        self.bag = rosbag.Bag(bag_name)
        self.topics = topics
        self.subtopics = subtopics
        self.save_prefix = save_prefix
        self.start_time = 0
        self.topic_lengths = {}#np.zeros(len(topics))
        self.get_bag_info_clean()
        
        for topic in topics:
            self.print_topic_example(topic)
        index = 0
        for (topic, msg, t) in self.bag.read_messages(topics=['/task_status']):
            index += 1
        print(index)
        print(self.topic_lengths)
        self.topic_into_nparray()
        self.bag.close()

    def get_bag_info_clean(self):
        info_dict = yaml.load(self.bag._get_yaml_info())
        self.start_time = info_dict['start']

        print("Printing information about topics with more than 1 messages")
        for item in info_dict['topics']:
            #if it's a topic I care about, tell me how many messages I have for np use
            if item['topic'] in self.topics:
                self.topic_lengths[item['topic']] = item['messages'] 
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

    def topic_into_nparray(self):

        for topic_index, topic in enumerate(self.topics):

            t_array = np.zeros(self.topic_lengths[topic])
            data_array = np.empty([len(self.subtopics[topic_index]), self.topic_lengths[topic]],dtype=object)
            time_index = 0
            for (unused,msg,t) in self.bag.read_messages(topics=[topic]):
                t_array[time_index] = t.secs + t.nsecs*1e-9
                for subtopic_index, subtopic in enumerate(self.subtopics[topic_index]):
                    data_array[subtopic_index,time_index] = operator.attrgetter(subtopic)(msg)
                    
                time_index += 1
        #save...
            filename = self.save_prefix + '_' + self.topics[topic_index][1:]   # skip the '/' at beginning of topic name
            np.save(filename, data_array)
            filename += '_time'
            np.save(filename, t_array)
            print(t_array)
            print(data_array)


