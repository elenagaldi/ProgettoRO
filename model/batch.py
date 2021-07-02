from model.job import Job
from model.task import Task


class Batch:
    def __init__(self, capacity, j_t: [[Job, Task]] = None, start=0):  # in ingresso prende una matrice 2xM, M numero
        # massimo di task processabili in un batch contemporaneamente
        self.j_t = j_t
        self.start = start
        self.capacity = capacity

    def get_max_dur(self):
        dur_max = 0
        for i in self.j_t:
            if dur_max < self.j_t[i][1].duration:
                dur_max = self.j_t[i][1].duration
        print(dur_max)
        return dur_max

    def empty_batch(self):
        return self.j_t == [[]] or not self.j_t

    def full_batch(self):
        return len(self.j_t) == self.capacity

    def is_job_in(self, job_id):
        # for i in range(len(self.j_t) - 1):
        #     if self.j_t[i][0].j_id == job_id:
        #         return True
        # return False
        return job_id in [x[0].id for x in self.j_t]

    def add_task(self, job, task):
        if not self.full_batch():
            self.j_t.append([job, task])

    def remove_task(self, job, task):
        if not self.empty_batch():
            for i in self.j_t:
                if self.j_t[i][0] == job and self.j_t[i][1] == task:
                    del self.j_t[i]

    def calc_end(self):
        return self.start + self.get_max_dur()
