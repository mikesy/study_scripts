#!/usr/bin/python3
""" 
This is an example of how to use the csv data to make yourself a checklist
Just a linear script since it's not meant to be portable
"""


def print_trial_header(tags):
    txt_str = "-----------------------------------------------------\n"
    for tag in tags:
        txt_str += tag + "\t"
    txt_str += "\n-----------------------------------------------------\n"
    return txt_str

def print_event(event_name, notes):
    txt_str = event_name + "\n"
    for note in notes:
        txt_str += "-- " + note+": \n"
    return txt_str
