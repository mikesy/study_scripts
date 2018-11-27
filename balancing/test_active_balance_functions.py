import unittest
import numpy as numpy
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
        self.assertEqual([1,2,0],order)

        #case with multiple solutions (but one where one is far behind and needs to be balanced)


        #case with multiple solutions