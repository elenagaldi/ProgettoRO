from model.task import Task
from bisect import bisect_left


class Batch:
    # j_t è una matrice 2XM che indica i task da inserire nel batch, M è la dimensione
    # massima del batch, ogni riga è formata da due elementi, il primo è un intero che indica l'id del job, il
    # secondo è un oggetto Task
    def __init__(self, id_batch, capacity, j_t: [(int, Task)] = None,
                 start=0):  # in ingresso prende una matrice 2xM, M numero
        # massimo di task processabili in un batch contemporaneamente
        self.id = id_batch
        self.j_t = j_t
        self.start = start
        self.capacity = capacity
        self.end = self.calc_end()

    def get_max_dur(self):
        if not self.empty_batch():
            dur_max = max([task[1].duration for task in self.j_t])
            return dur_max
        else:
            return 0

    def get_longest_task(self):
        if not self.empty_batch():
            return max([task for task in self.j_t], key=lambda t: t[1].duration)
        else:
            return None

    def get_latest_reltime(self, jobs_dict):
        if len(self.j_t) == 0:
            return 0
        else:
            return max([jobs_dict[task[0]].release_time for task in self.j_t])

    def empty_batch(self):
        return self.j_t == [[]] or not self.j_t

    def full_batch(self):
        return len(self.j_t) == self.capacity

    def is_job_in(self, job_id):
        return job_id in [x[0] for x in self.j_t]

    def add_task(self, job: int, task: Task):
        # if not self.full_batch():
        #     ##inserisce il task in ordine di durata nel batch
        #     # durations = [jt[1].duration for jt in self.j_t]
        #     # i = bisect_left(durations, task.duration)
        #     # self.j_t.insert(i, [job, task])
        self.j_t.append((job, task))
        self.end = self.calc_end()

    def add_task2(self, jt: (int, Task)):
        self.add_task(jt[0], jt[1])

    def remove_task(self, job: int, task: Task):
        self.j_t.remove((job, task))
        self.end = self.calc_end()

    def remove_taskv2(self, jt: int):
        del self.j_t[jt]

    def remove_taskv3(self, jt: (int, Task)):
        self.remove_task(jt[0], jt[1])

    def calc_end(self):
        end = self.start + self.get_max_dur()
        return end

    def analyze_task_duration_diff(self):
        # aux, weight = 0, 1
        # for jt1, jt2 in zip(self.j_t[0::1], self.j_t[1::1]):
        #     auxTemp = abs(jt1[1].duration - jt2[1].duration) * weight
        #     weight += 1 if auxTemp > 0 else 0
        #     aux = aux + auxTemp
        diff = 0
        longest_task = (self.get_longest_task())[1]
        for jt in self.j_t:
            diff += longest_task.duration - jt[1].duration
        return diff

    def __repr__(self):
        return f'"Batch {self.id} : {[(x[0], x[1].id) for x in self.j_t]} Start:{self.start} End: {self.end}"\n'

    def __str__(self):
        return self.__repr__()

    def update_time(self, start):
        self.start = start
        self.end = self.calc_end()

    def __eq__(self, other):
        if not isinstance(other, Batch):
            # don't attempt to compare against unrelated types
            return NotImplemented

        for jt1, jt2 in zip(self.j_t, other.j_t):
            if jt1[0] != jt2[0] or jt1[1].id != jt2[1].id:
                return False
        return True
