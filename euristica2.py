from model.batch import Batch
from model.job import Job


class Greedy2:
    def __init__(self, jobs: [Job], capacity_batch, tot_task):
        self.jobs = jobs
        self.tot_task = tot_task
        self.m = capacity_batch

    def start(self):
        batches = self.labeling()
        return batches

    def labeling(self):
        lista_task = []
        for i in self.jobs:
            for j in range(len(i.task)):
                lista_task.append([i.id, i.release_time, i.task[j]])

        lista_task.sort(key=lambda x: x[1])
        lista_task.sort(key=lambda x: x[2].duration, reverse=True)

        len_tasks = len(lista_task)
        task_i = 0
        j_t = []
        batches: [Batch] = []
        # print(lista_task[task_i][0])
        start_next_batch = self.jobs[lista_task[task_i][0]].release_time

        id_batch = 0

        while task_i < len_tasks - 1:
            k = 0
            while k in range(self.m) and self.jobs[lista_task[task_i][0]].release_time <= start_next_batch:
                if not lista_task[task_i][2].processed:
                    for t in self.jobs[lista_task[task_i][0]].task:
                        if t.id == lista_task[task_i][2].id:
                            j_t.append([lista_task[task_i][0], t])
                            t.set_processed(True)
                            if self.jobs[lista_task[task_i][0]].is_completed():
                                self.jobs[lista_task[task_i][0]].last_batch = id_batch
                            k += 1
                if task_i < len_tasks - 1:
                    task_i += 1
                else:
                    break

            batch = Batch(id_batch, self.m, j_t, start_next_batch)
            batches.append(batch)
            start_next_batch = max(batch.end, self.jobs[lista_task[task_i][0]].release_time)
            j_t = []
            id_batch += 1

        print(f'Batches : {batches}')
        return batches
