from task import *
from array import array

# =list(range(input.k))

class Job:
    def __init__(self, j_id, release_time, due_date, task, last_batch=0):
        self.id = j_id
        self.release_time = release_time
        self.due_date = due_date
        self.task = task
        self.last_batch = last_batch

    def set_task_on(self, index):
        self.task[index].set_state(True)

    def set_task_off(self, index):
        self.task[index].set_state(False)

    def get_task(self, index):
        return self.task[index].state

    def get_id(self):
        return self.id

    def find_st(self):  # find shortest task
        length = 1000
        index = 0
        for i in range(len(self.task)):
            if length > self.task[i].duration:
                length = self.task[i].duration
                index = i
        return i  # ritorna l'indice del task con durata minore

    def find_lt(self):  # find longest task
        length = 0
        index = 0
        i = 0
        for i in range(len(self.task)):
            if length < self.task[i].duration:
                length = self.task[i].duration
                index = i
        return i  # ritorna l'indice del task con durata maggiore
