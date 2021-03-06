# =list(range(input.k))
from model.task import Task


class Job:
    def __init__(self, j_id, release_time, due_date, task: [Task] = None):
        self.id = j_id
        self.release_time = release_time
        self.due_date = due_date
        self.task = task
        self.last_batch = None
        self.delay = None

    def set_task_on(self, index):
        self.task[index].set_processed(True)

    def set_task_off(self, index):
        self.task[index].set_processed(False)

    def get_task(self, index):
        return self.task[index].processed

    def get_id(self):
        return self.id

    def find_shortest_task_notprocessed(self):  # find shortest task
        return min([task for task in self.task if not task.is_processed()], key=lambda t: t.duration)

    def find_longest_tast_notprocessed(self):  # find longest task
        return max([task for task in self.task if not task.is_processed()], key=lambda t: t.duration)

    def is_completed(self):
        for x in self.task:
            if x.processed is False:
                return False
        else:
            return True

    def sum_dur_task(self):
        return sum(t.duration for t in self.task)

    def __repr__(self):
        return f'ID:{self.id} Realease time:{self.release_time} Due date: {self.due_date} Task : {[t.id for t in self.task]}\n '

    def __str__(self):
        return self.__repr__()

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Job):
            return self.__key() == other.__key()
        return NotImplemented
