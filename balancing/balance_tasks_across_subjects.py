from sys import argv
import numpy as np
import random



class randomlyBalanceExp(object):
    """docstring for randomlyBalanceExp."""
    def __init__(self, arg):
        self.num_subjects = int(arg[1])
        self.num_tasks = int(arg[2])
        print("You specified", self.num_subjects, "subjects and", self.num_tasks, "tasks")
        self.getExpTask()

    def getExpTask(self):
        task_count =  np.zeros([self.num_tasks,self.num_tasks])  #row is task and column is count of times used in that position
        task_array = np.zeros([self.num_subjects,self.num_tasks])
        balancing_tol = 2
        sub_i = 0

        while sub_i < self.num_subjects:
            task_order = self.getSemiRandPerm(task_count)
            temp_task_count = np.copy(task_count)
            for task_i in range(self.num_tasks):
                temp_task_count[task_i,np.where(task_order==task_i)[0][0]] += 1

            if (np.amax(temp_task_count)-np.amin(temp_task_count)) < balancing_tol: #within bounds of balancing tolerance
                task_count = temp_task_count
                task_array[sub_i,:] = task_order
                sub_i += 1 # move on to next subject
        print("This is the task count.... each row is the task and the column represents the amount the task has been in that position")
        print(task_count)
        print("The task array... each row is a subject corresponding to a task sequence")
        print (task_array+1)


    def getTaskCount(self,sub_tasks):
        tc =  np.zeros([self.num_tasks,self.num_tasks])  #tc = task count
        for task_set in sub_tasks:
            for task in task_set:
                tc[int(task), np.where(task_set==task)[0][0]] += 1
        return tc

    def getSemiRandPerm(self,count_array):
        task_set_found = False
        min_count = np.min(count_array)
        remaining_positions = [i for i in range(0,self.num_tasks)]
        task_set_2 = np.empty(self.num_tasks)

        a = np.where(count_array==min_count)
        num_mins = np.size(a[0])

        min_by_task = []
        for task in range(0,self.num_tasks):
            min_task = []
            for a_i in range(0,num_mins):
                if a[0][a_i] == task:
                    min_task.append(a[1][a_i])
            min_by_task.append(min_task)    #each row is the task and each element of the row is the position which is a minimum

        while(not task_set_found):
            remaining_positions = [i for i in range(0,self.num_tasks)]
            for task in range(0,self.num_tasks):
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
                if task == (self.num_tasks-1):
                    task_set_found = True
                remaining_positions = remaining_positions[0:remaining_positions.index(task_position)] + remaining_positions[(remaining_positions.index(task_position)+1):]
        return task_set_2


if __name__ =="__main__":
    rbe = randomlyBalanceExp(argv)