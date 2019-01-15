#!/usr/bin/python


# if you feed multiple bags into the bag object, it will combine them using their start times
# it assumes you put the bags in order starting from the first (earliest) bag

import rosbag
import yaml
import numpy as np
import operator      #makes it easier to pull sub-topics using attrgetter


class bagObject:
    def __init__(self,bag_names,topics, subtopics,save_prefix):

        # initialize 
        self.bags = self.bags_into_array(bag_names)
        self.topics = topics
        self.subtopics = subtopics
        self.save_prefix = save_prefix
        self.start_times = []
        self.info_dicts = []
        self.topic_lengths = []

        #do stuff
        self.bags_into_array(bag_names)
        self.preprocess()
        self.convert_topics_to_nparray()

    def __del__(self):  # close the bags of destruction
        self.close_bags()

    ## main functions that processes all the topics
    def bags_into_array(self,bag_names):
        bags = []
        for bag_name in bag_names:
            bags.append(rosbag.Bag(bag_name))
        return bags

    def preprocess(self): # all info necessary to cycle through all topics 
        for bag in self.bags:
            info_dict = yaml.load(bag._get_yaml_info())
            self.info_dicts.append(info_dict)
            topic_length_dict = {}
            for item in info_dict['topics']:
                #if it's a topic I care about, tell me how many messages I have for np use
                if item['topic'] in self.topics:
                    topic_length_dict[item['topic']] = item['messages']
            self.topic_lengths.append(topic_length_dict)
            self.start_times.append(info_dict['start'])
        self.start_time_check()

    ## functions to provide user with info about the bag, to be called in separate script
    def get_bag_info_clean(self):
        print("Printing information about topics with more than 1 messages")
        for item in self.info_dicts[0]['topics']:
            if (item['messages'] > 1): 
                print("------------")
                print("topic name: " + item['topic'] + " \t type: " + item['type'])
                print("number of messages  = " + str(item['messages']) +  " at a rate of " + str(item['frequency']) + "Hz")
        print("------------")

    def print_topic_example(self, topic_name):
        print("------------")
        print("An example message of topic: " + topic_name)
        for (topic, msg, t) in self.bags[0].read_messages(topics=[topic_name]):
            print(msg)
            break
        print("------------")

    def convert_topics_to_nparray(self):
        for topic_index, topic in enumerate(self.topics):
            total_topic_length = self.get_total_topic_length(topic)
            t_array = np.zeros(total_topic_length)
            data_array = np.empty([total_topic_length, len(
                self.subtopics[topic_index])], dtype=object)
            time_index = 0
            for bag in self.bags:
                for (unused,msg,t) in bag.read_messages(topics=[topic]):
                    t_array[time_index] = t.secs + t.nsecs*1e-9
                    for subtopic_index, subtopic in enumerate(self.subtopics[topic_index]):
                        data_array[time_index, subtopic_index] = operator.attrgetter(
                            subtopic)(msg)
                        
                    time_index += 1
        #save...
            filename = self.save_prefix + '_' + self.topics[topic_index][1:]   # skip the '/' at beginning of topic name
            np.save(filename, data_array)
            filename += '_time'
            np.save(filename, t_array)

    def get_total_topic_length(self, topic):
        topic_length_total = 0
        for topic_length_dict in self.topic_lengths:
            topic_length_total += topic_length_dict[topic]
        return topic_length_total
    ## checks and misc
    def start_time_check(self):
        for st in self.start_times[1:]:
            if st < self.start_times[0]:
                raise ValueError("The bags you passed are out of order")
    
    def close_bags(self):
        for bag in self.bags:
            bag.close()
