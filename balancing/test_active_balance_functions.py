import unittest
import numpy as np
from active_balance_functions import *

class ActiveBalaceTestCase(unittest.TestCase):
    """tests for active_balanace.py"""

    def test_get_next_balance(self):
        # initial case
        count = np.zeros((3,3))

        # case where all tied (same as initial in theory)
        count = np.ones((5,5))*9

        # case with single solution
        count = np.array([[1,0,0],[0,1,1],[1,0,1]])
        order = get_next_balance(count)
        print("order", order)
        # self.assertEqual([2,0,1],order)

        #case with multiple solutions (but one where one is far behind and needs to be balanced)


        #case with multiple solutions
    def test_get_all_combos_from_initial_set(self):
        feature_set = [1,2]
        remaining_features = [0,4]
        correct_response = [[1,2,0,4],[1,2,4,0]]
        self.assertEqual(get_all_combos_from_initial_set(
            feature_set, remaining_features), correct_response)


        feature_set = [0,1]
        remaining_features = [2]
        correct_response = [[0,1,2]]
        self.assertEqual(get_all_combos_from_initial_set(
            feature_set, remaining_features), correct_response)

    def test_get_feature_set(self):
        order_array = [2,0,1]
        feature_set = [1,2,0]
        self.assertEqual(get_feature_set(order_array),feature_set)

        with self.assertRaisesRegex(ValueError, "Array does not contain unique values between 0 and N"):
            order_array = [0,0,1]
            get_feature_set(order_array)

    def test_get_all_combos_by_position_mins(self):
        count = np.array([[1,1,1],[2,0,1],[2,1,0]])
        correct_response = [[0,1,2]]
        self.assertEqual(get_all_combos_by_position_mins(count),correct_response)

        #case where no possible solutions exist
        count = np.array([[0, 3, 0], [2, 0, 1], [1, 0, 2]])
        correct_response = []
        self.assertEqual(get_all_combos_by_position_mins(count), correct_response)

    def test_get_next_min(self):
        a = [0,1,2]
        offset = 0
        correct_response = 0
        self.assertEqual(get_next_min(a,offset),correct_response)

        a = [2,1,0]
        offset = 0
        correct_response = 0
        self.assertEqual(get_next_min(a, offset), correct_response)

        a = [2, 1, 0, 4]
        offset = 1
        correct_response = 1
        self.assertEqual(get_next_min(a, offset), correct_response)

        with self.assertRaisesRegex(ValueError, "Min offset too large for this array"):
            a = [2, 1, 0, 2]
            offset = 4
            correct_response = 1
            get_next_min(a, offset)

    def test_balance_first_pos_priority(self):
        count = np.array([[1, 1, 1], [2, 0, 1], [2, 1, 0]])
        correct_response = [0,1,2]
        self.assertEqual(balance_first_pos_priority(count),correct_response)

        count = np.array([[0, 3, 0], [2, 0, 1], [1, 0, 2]])
        correct_response = [0, 2, 1]
        self.assertEqual(balance_first_pos_priority(count), correct_response)

        # case where we need to relax the last position min
        count = np.array([[1, 2, 2], [2, 1, 0], [2, 2, 1]])
        correct_response = [0, 1, 2]
        self.assertEqual(balance_first_pos_priority(count), correct_response)

        
