import input
from task import *
from numpy import array


class Job:
    def __init__(self, id, release_time, due_date, task=list(range(input.k))):
        self.id = id
        self.release_time = release_time
        self.due_date = due_date
        self.task = task

    def set_task_on(self, index):
        self.task[index].set_state(True)

    def set_task_off(self,index):
        self.task[index].set_state(False)

    def get_task(self, index):
        return self.task[index].state

    def get_id(self):
        return self.id

    def find_ST(self): # find shortest task
        length = 1000
        index = 0
        for i in range(input.k):
            if length > self.task[i].duration:
                length = self.task[i].duration
                index = i
        return i  # ritorna l'indice del task con durata minore

    def find_LT(self): # find longest task
        length = 0
        index = 0
        i = 0
        for i in range(input.k):
            if length < self.task[i].duration:
                length = self.task[i].duration
                index = i
        return i  # ritorna l'indice del task con durata maggiore
