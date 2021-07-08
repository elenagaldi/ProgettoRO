# =list(range(input.k))
from model.task import Task


class Job:
    def __init__(self, j_id, release_time, due_date, task: [Task] = None, last_batch=0):
        self.id = j_id
        self.release_time = release_time
        self.due_date = due_date
        self.task = task
        self.last_batch = last_batch

    def set_task_on(self, index):
        self.task[index].set_processed(True)

    def set_task_off(self, index):
        self.task[index].set_processed(False)

    def get_task(self, index):
        return self.task[index].processed

    def get_id(self):
        return self.id

    def find_st(self):  # find shortest task
        return min(self.task, key=lambda t: t.duration)

    def find_lt(self):  # find longest task
        return max(self.task, key=lambda t: t.duration)

    def is_completed(self):
        for x in self.task:
            if x.processed is False:
                return False
        else:
            return True

    def __repr__(self):
        return f'Job ID:{self.id} Realease time:{self.release_time} Due date: {self.due_date} Task : [{self.task}]\n'

    def __str__(self):
        return self.__repr__()
