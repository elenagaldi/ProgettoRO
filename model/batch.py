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




