from model.batch import Batch
from model.job import Job


class Greedy:
    def __init__(self, jobs: [Job], capacity_batch, tot_task):
        self.jobs = jobs
        self.m = capacity_batch
        self.tot_task = tot_task

    def start(self):
        batches = self.labeling()
        return batches

    def labeling(self):
        self.jobs.sort(key=lambda x: x.release_time)

        task_i = 0
        j_t = []
        batches: [Batch] = []
        tasks_processed = 0
        id_batch = 0
        self.jobs.sort(key=lambda x: x.due_date)
        length = len(self.jobs)
        middle_index = length // 2
        prima_meta = self.jobs[:middle_index]
        seconda_meta = self.jobs[middle_index:]
        prima_meta.sort(key=lambda x: x.release_time)
        seconda_meta.sort(key=lambda x: x.release_time)
        print(prima_meta)
        print('Le differenze\n')
        print(seconda_meta)
        z = len(prima_meta)
        y = len(seconda_meta)
        num_jobs = z
        # Qui conto quanti sono i task dentro ogni lista
        primi_task = []
        print(prima_meta)

        for i in prima_meta:
            for t in i.task:
                primi_task.append([i.id, t.duration])

        primi_task.sort(key=lambda x: x[1])
        print(primi_task)

        secondi_task = []

        for i in seconda_meta:
            for t in i.task:
                secondi_task.append([i.id, t.duration])
        secondi_task.sort(key=lambda x: x[1])
        print(secondi_task)

        job = self.jobs[primi_task[task_i][0]]
        start_next_batch = job.release_time

        while tasks_processed < len(primi_task):
            k = 0
            while k in range(self.m) and self.jobs[primi_task[task_i][0]].release_time <= start_next_batch and tasks_processed < len(primi_task):
                for t in self.jobs[primi_task[task_i][0]].task:
                    print(t.duration, primi_task[task_i][0], primi_task[task_i][1])
                    if t.duration == primi_task[task_i][1] and not t.is_processed:
                        # if not t.is_processed():
                        j_t.append([primi_task[task_i][0], t])
                        t.set_processed(True)
                        if self.jobs[primi_task[task_i][0]].is_completed():
                            self.jobs[primi_task[task_i][0]].last_batch = id_batch
                        k += 1
                        task_i += 1
            batch = Batch(id_batch, self.m, j_t, start_next_batch)
            batches.append(batch)
            start_next_batch = max(batch.end, job.release_time)
            j_t = []
            id_batch += 1
         #commento per push.
        print(f'Batches : {batches}')

        # Qui conto quanti sono i task dentro ogni lista
        primi_task = []
        print(prima_meta)

        for i in prima_meta:
            for t in i.task:
                primi_task.append([i.id, t.duration])

        primi_task.sort(key=lambda x: x[1])
        print(primi_task)

        secondi_task = []

        for i in seconda_meta:
            for t in i.task:
                secondi_task.append([i.id, t.duration])
        secondi_task.sort(key=lambda x: x[1])
        print(secondi_task)

        return batches
