#!/usr/bin/python3

from sys import argv
import numpy as np
import random
import argparse

class randomlyBalanceExp(object):
    """docstring for randomlyBalanceExp.
        IMPORTANT: This assumes all features are independent
        NOTE: please verify the balancing by hand, at least for a small case to enure this works for your scenario as I haven't tested all cases
    """
    
    def __init__(self, num_subjects, tasks_per_subject, num_levels, features_per_level):
        self.num_subjects = num_subjects
        self.tasks_per_subject = tasks_per_subject
        self.num_levels = num_levels
        self.features_per_level = features_per_level
        print("You specified", self.num_subjects, "subjects and", self.num_levels, "levels with the following features per level: " , features_per_level)
        self.getExpTask()
        self.task_count = []
        self.task_array = []

    def getExpTask(self):
        balancing_tol = 2
        sub_i = 0
        task_count = []
        task_array = []
        task_count.append(np.zeros([self.features_per_level[0], self.features_per_level[0]]))
        task_array.append(np.zeros([self.num_subjects, self.features_per_level[0]]))
        for i in range(1,self.num_levels):
            task_count.append(np.zeros([self.features_per_level[i], self.features_per_level[i]]))
            task_array.append(np.zeros([self.num_subjects, self.features_per_level[i]]))
        
        for level_i, features_in_level in enumerate(self.features_per_level):
            sub_i = 0
            while sub_i < self.num_subjects:
                task_order = self.getSemiRandPerm(task_count[level_i],features_in_level)
                temp_task_count = np.copy(task_count[level_i])   #copy may not be necessary here as it was in 1 level case
                for task_i in range(features_in_level):
                    temp_task_count[task_i, np.where(task_order == task_i)[0][0]] += 1

                # within bounds of balancing tolerance
                if (np.amax(temp_task_count)-np.amin(temp_task_count)) < balancing_tol:
                    task_count[level_i] = temp_task_count
                    task_array[level_i][sub_i, :] = task_order
                    sub_i += 1  # move on to next subject
        
        #trim based on number of tasks per subject
        for i in range(self.num_levels):
            task_count[i] = task_count[i][:,0:self.tasks_per_subject]
            task_array[i] = task_array[i][:, 0:self.tasks_per_subject]
        self.print_results(task_count, task_array)

    def getSemiRandPerm(self,count_array,task_num):
        task_set_found = False
        min_count = np.min(count_array)
        
        task_set_2 = np.empty(task_num)
        a = np.where(count_array==min_count)
        num_mins = np.size(a[0])

        min_by_task = []
        for task in range(0,task_num):
            min_task = []
            for a_i in range(0,num_mins):
                if a[0][a_i] == task:
                    min_task.append(a[1][a_i])
            min_by_task.append(min_task)    #each row is the task and each element of the row is the position which is a minimum

        while(not task_set_found):
            remaining_positions = [i for i in range(0,task_num)]
            for task in range(0,task_num):
                if not min_by_task[task]:
                    print("Need further development for this scenario (not sure it well ever exist as long as tolerance is 2)")
                    return 0
                rand_index = random.randrange(len(min_by_task[task]))
                # create a list of possible matches between minumums and available positions
                match_mins = list(set(min_by_task[task]).intersection(remaining_positions))
                if not match_mins:
                    break
                rand_index = random.randrange(len(match_mins))
                task_position = match_mins[rand_index]
                task_set_2[task_position] = task
                if task == (task_num-1):
                    task_set_found = True
                remaining_positions = remaining_positions[0:remaining_positions.index(task_position)] + remaining_positions[(remaining_positions.index(task_position)+1):]
        return task_set_2
    
    def print_results(self, task_count, task_array):
        print("This is the task count.... each row is the task and the column represents the amount the task has been in that position")
        print(task_count)
        print("The task array... each row is a subject corresponding to a task sequence")
        print(task_array)

        for i in range(self.num_levels):
            filename = "feature%i.csv" % i
            np.savetxt(filename , task_array[i],delimiter=',')
            print("results of feature",i, "have been printed to", filename)
        print("rows are each subject where the elements represent the task order (left to right) for each subject")
        
if __name__ =="__main__":
    parser=argparse.ArgumentParser()

    parser.add_argument('subjects', type=int, help='number of subjects to balance across') 
    parser.add_argument('tasks_per_subject',type=int, help='number of tasks each subject will perform (does not need to be the same as number of levels per a task')
    parser.add_argument('levels', type=int, help='define number of levels of balancing')
    parser.add_argument('feature_num',type=str, help='an array that defines the number of features to balance at each level, type as 2,3,1')

    args = parser.parse_args()
    feature_nums = list(map(int,args.feature_num.split(',')))


    rbe = randomlyBalanceExp(args.subjects, args.tasks_per_subject, args.levels, feature_nums)
