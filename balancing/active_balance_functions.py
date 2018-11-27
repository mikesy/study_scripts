import numpy as np
import random

def get_next_balance(count_array):
    count_array_shape = np.shape(count_array)
    features = count_array_shape[1]
    positions = count_array_shape[0]

    
    min_in_positions = np.amin(count_array, axis=1)
    print("min in positions", min_in_positions)
    # positions_available = np.array(range(positions))
    looking = True
    while(looking):
        # positions_available = np.array(range(positions))
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
                break
            rand_index = random.randrange(len(mins_avail))
            feature = mins_avail[rand_index]
            # print("pos avail", positions_available)
            # print(feature)
            #positions_available = positions_available[0:feature] + positions_available[feature+1:]
            print("feature chosen", feature)
            positions_available = [i for i in positions_available if i!=feature]
            # positions_available = np.delete(
                # positions_available, feature)  # .remove(feature)
            feature_order.append(feature)
            

            print("mins", mins[0])
            print("features", feature_order)
            print("mins avail", mins_avail)
            print("pos avail", positions_available)

            if i == positions-1:
                looking = False

        # looking = False
    return feature_order
