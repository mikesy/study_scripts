import numpy as np
import random
from math import factorial

def get_next_balance(count_array):
    """ returns """
    count_array_shape = np.shape(count_array)
    features = count_array_shape[0]
    positions = count_array_shape[1]
    # max_combos = get_max_combos_using_mins(count_array)
    combos_used = []
    min_in_positions = np.amin(count_array, axis=1)
    looking = True
    while(looking):
        positions_available = range(positions)
        feature_order = []
        for i in range(positions):
            mins = np.where(count_array[i, :] == min_in_positions[i])
            mins_avail = []
            for m in mins[0]:
                print(m)
                if m in positions_available:
                    mins_avail.append(m)
            if len(mins_avail) == 0:
                print("issue finding enough mins available, restarting looking")
                #add remaining combos from this position on bc none are valid and add to combos used
                additional_combos = get_all_combos_from_initial_set(feature_order,positions_available)
                for combo in additional_combos:
                    combos_used = check_combo_used(combo,combos_used)
                print(combos_used)
                break

            rand_index = random.randrange(len(mins_avail))
            feature = mins_avail[rand_index]
            print("feature chosen", feature)
            positions_available = [i for i in positions_available if i!=feature]
            feature_order.append(feature)
            

            print("mins", mins[0])
            print("features", feature_order)
            print("mins avail", mins_avail)
            print("pos avail", positions_available)

            # if len(combos_used) >= max_combos:
            #     print("used all combos, prioritizing the first slot first")
  
            if i == positions-1:
                looking = False
        looking = False
    return feature_order


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


def get_feature_set(order_array):
    """ inputs
        order_array = each element corresponds to the feature and...
                      the value is position seen in the experiment
    """
    #check input is valid
    num_features = len(order_array)-1
    if int(num_features*(num_features+1)/2) != sum(order_array):
        raise ValueError("Array does not contain unique values between 0 and N")

    # get feature set and return
    feature_set = [0]*len(order_array)
    for feature, pos in enumerate(order_array):
        feature_set[pos] = feature
    return feature_set

def check_combo_used(current_combo, combos_used_array):
    not_used = True
    for combo in combos_used_array:
        if combo == current_combo:
            not_used = False
            break
    if not_used:
        combos_used_array.append(current_combo)
    return combos_used_array

def get_all_combos_from_initial_set(current_feature_set, remaining_features):
    combos = []
    num_remaining = len(remaining_features)
    for i in range(num_remaining):
        combo = current_feature_set + [remaining_features[i]]
        for j in range(num_remaining):
            if i !=j:
                combo.append(remaining_features[j])
        combos.append(combo)
    print("COMBOS", combos)
    return combos

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
