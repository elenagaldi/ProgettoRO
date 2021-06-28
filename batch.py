import input
from job import *
from task import *
from numpy import array


class Batch:
    def __init__(self, j_t=None, start=0):  # in ingresso prende una matrice 2xM, M numero
        # massimo di task processabili in un batch contemporaneamente
        self.j_t = j_t
        self.start = start

    def get_max_dur(self):
        dur_max = 0
        for i in range(len(self.j_t)):
            if dur_max < self.j_t[i][1].duration:
                dur_max = self.j_t[i][1].duration
        print(dur_max)
        return dur_max

    def empty_batch(self):
        if len(self.j_t) == 0:
            return True
        return False

    def full_batch(self):
        if len(self.j_t) == input.M:
            return True
        return False

    def is_job_in(self, job_id):
        for i in range(len(self.j_t)-1):
            if self.j_t[i][0].j_id == job_id:
                return True
        return False

    def add_task(self, job, task):
        if not self.full_batch():
            self.j_t.append([job, task])

    def remove_task(self, job, task):
        if not self.empty_batch():
            for i in range(len(self.j_t)):
                if self.j_t[i][0] == job and self.j_t[i][1] == task:
                    del self.j_t[i]

    def calc_end(self):
        return self.start + self.get_max_dur()


'''
class Batch:
    def __init__(self, start=0, j=array(range(input.M)), t=array(range(input.M))): # in ingresso prende un array di indici di job ed un array di indici di task
        self.j = j  # tengo memoria dei job a cui appartengono i task
        self.t = t  # per ogni job tengo memoria dei task nel batch
        self.start = start

    def calcola_durata(self):
        durata_max = 0
        for i in range(input.M):
            if durata_max < input.duration_t[self.t[i]]:
                durata_max = input.duration_t[self.t[i]]

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
'''

