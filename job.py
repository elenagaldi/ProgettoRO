# =list(range(input.k))

class Job:
    def __init__(self, j_id, release_time, due_date, task=None, last_batch=0):
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
        shortest = self.task[0]
        for i in range(1, len(self.task)):
            next_task = self.task[i]
            if next_task.duration < shortest.duration:
                shortest = next_task
        return shortest
    
    # alternativa
    def find_st2(self):
        return min(self.task, key=lambda t: t.duration)

    def find_lt(self):  # find longest task
        longest = self.task[0]
        for i in range(1, len(self.task)):
            next_task = self.task[i]
            if next_task.duration > longest.duration:
                longest = next_task
        return longest

    # alternativa
    def find_lt2(self):
        return max(self.task, key=lambda t: t.duration)
