"""
functions used in active_balance.py and balance_tasks_across_subjects.py
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
