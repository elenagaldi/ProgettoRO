from model.task import Task


class Batch:
    # j_t è una matrice 2XM che indica i task da inserire nel batch, M è la dimensione
    # massima del batch, ogni riga è formata da due elementi, il primo è un intero che indica l'id del job, il
    # secondo è un oggetto Task
    def __init__(self, id_batch, capacity, j_t: [[int, Task]] = None,
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

    def empty_batch(self):
        return self.j_t == [[]] or not self.j_t

    def full_batch(self):
        return len(self.j_t) == self.capacity

    def is_job_in(self, job_id):
        return job_id in [x[0] for x in self.j_t]

    def add_task(self, job: int, task):
        if not self.full_batch():
            self.j_t.append([job, task])
            self.end = self.calc_end()

    def remove_task(self, job: int, task):
        if not self.empty_batch():
            for x in self.j_t:
                if x[0] == job and x[1] == task.id:
                    del self.j_t[self.j_t.index(x)]
            self.end = self.calc_end()

    def calc_end(self):
        end = self.start + self.get_max_dur()
        return end

    def __repr__(self):
        return f'"Batch {self.id} : {[(x[0], x[1].id) for x in self.j_t]} Start:{self.start} End: {self.end}"\n'

    def __str__(self):
        return self.__repr__()
