from model.batch import Batch
from model.job import Job


class Greedy2:
    def __init__(self, jobs: [Job], lista_task, capacity_batch):
        self.jobs = jobs
        self.tasks = lista_task
        self.m = capacity_batch

    def start(self):
        batches = self.labeling()
        return batches

    def labeling(self):
        self.tasks.sort(key=lambda x: x[1])
        self.tasks.sort(key=lambda x: x[2].duration, reverse=True)

        print(f'Tasks:\t {self.tasks}')
        len_tasks = len(self.tasks)
        task_i = 0
        j_t = []
        batches: [Batch] = []

        start_next_batch = self.jobs[self.tasks[task_i][0]].release_time

        id_batch = 0

        while task_i < len_tasks - 1:
            k = 0
            while k in range(self.m) and self.jobs[self.tasks[task_i][0]].release_time <= start_next_batch and task_i < len_tasks - 1:
                for t in self.jobs[self.tasks[task_i][0]].task:
                    if t.t_id == self.tasks[task_i][2].t_id:
                        # if not t.is_processed():
                        j_t.append([self.tasks[task_i][0], t])
                        t.set_processed(True)

                        if self.jobs[self.tasks[task_i][0]].is_completed():
                            self.jobs[self.tasks[task_i][0]].last_batch = id_batch
                        k += 1
                        task_i += 1

            batch = Batch(id_batch, self.m, j_t, start_next_batch)
            batches.append(batch)
            start_next_batch = max(batch.end, self.jobs[self.tasks[task_i][0]].release_time)
            j_t = []
            id_batch += 1

        print(f'Batches : {batches}')
        return batches
