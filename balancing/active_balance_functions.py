"""
this is a series of functions use in active balancing scripts

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
"""

import numpy as np
import random
from math import factorial

def get_all_combos_by_position_mins(count_array, min_in_positions=[]):
    """ 
    inputs: 
        count_array- rows are features and columns are positions, 
                     each element represents the number of times the feature 
                     appeared in the position
        min_in_positions- (optional) if not specified, will use absolute minimum. 
                          if specified (for a case where you want to use a different value than abs min,
                          i.e. there were no possible combos with abs min),
                          it will use the minimum for each position specified
    outputs:
        filtered_combos- all possible combos using only minimums for each position
    """

    count_array_shape = np.shape(count_array)
    num_positions = count_array_shape[1]
    all_combos = []
    if len(min_in_positions) == 0:
        # use absolute minimum
        min_in_positions = np.amin(count_array, axis=0) 

    # initialize 
    for feature, pos_count in enumerate(count_array[:,0]):
        if pos_count == min_in_positions[0]:
            all_combos.append([feature])

    pos_i = 1        
    while pos_i != num_positions:
        for feature, pos_count in enumerate(count_array[:,pos_i]):
            # if this pos count is a minimum for the position
            if pos_count == min_in_positions[pos_i]:
                #if the feature is already in the combo, discard it; otherwise use it as a unique combo
                for combo in all_combos:
                    if len(combo) == pos_i: ## only add if not ahead of this step (i.e. from a previous min in this step)
                        if feature not in combo:
                            all_combos.append(combo + [feature])
        pos_i += 1
                        
    #required in case there are not any valid combos for the entire feature space
    filtered_combos = []
    for combo in all_combos:
        if len(combo) == num_positions:
            filtered_combos.append(combo)

    return filtered_combos
    
def get_next_min(a, min_offset):
    """
    inputs:
        a- array to search for Nth lowest value
        min_offset =  N where N corresponds to the Nth lowest value in the vector v.
    output:
        min_n = Nth lowest value in vector
    """
    
    min_val = 0
    for i in range(min_offset+1):
        min_val = min(a)
        a = [i for i in a if i != min_val]
        if len(a) == 0:
            raise ValueError("Min offset too large for this array")

    return min_val

def balance_first_pos_priority(count_array):
    min_in_positions_initial = np.amin(count_array, axis=0)
    min_in_positions = min_in_positions_initial
    max_in_positions = np.amax(count_array, axis=0)
    relaxing_index = -1

    all_combos = []
    while len(all_combos) == 0:
        all_combos = get_all_combos_by_position_mins(count_array,min_in_positions=min_in_positions)
        if min_in_positions[relaxing_index] == max_in_positions[relaxing_index]:
            relaxing_index -= 1
            min_in_positions = min_in_positions_initial

        min_in_positions[relaxing_index] += 1
    
    rand_index = random.randrange(len(all_combos))
    combo = all_combos[rand_index]
    return combo
