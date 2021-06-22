import input
from numpy import array

class Batch:
    def __init__(self, start=0, jt , j=array(range(input.M)), t=array(range(input.M))): # in ingresso prende un array di indici di job ed un array di indici di task
        self.j = j  # tengo memoria dei job a cui appartengono i task
        self.t = t  # per ogni job tengo memoria dei task nel batch
        self.start = start

    def calcola_durata(self):
        durata_max = 0
        for i in range(input.M):
            if durata_max < input.task_d[self.t[i]]:
                durata_max = input.task_d[self.t[i]]

        print(durata_max)
        return durata_max

    def empty_batch(self):
        for i in range(input.M):
            if self.j[i]:
                return False
        return True

    def full_batch(self):
        for i in range(input.M):
            if not self.j[i]:
                return False
        return True

    def is_job_in(self, job):
        for i in range(input.M):
            if self.j[i]==job:
                return True
        return False

    def set_task(self, job, task):
        if not self.full_batch():
            self.j.__add__(job)
            self.t.__add__(task)

    def remove_task(self, job, task):
        for i in range(input.M):
            if self.j[i]==job and self.t[i]==task:
                del self.j[i]
                del self.t[i]

    def calcola_fine(self):
        return self.start + self.calcola_durata()


