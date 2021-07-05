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
        num_jobs = len(self.jobs)
        job_i = 0
        task_i = 0
        j_t = []
        batches: [Batch] = []

        job = self.jobs[job_i]
        start_next_batch = job.release_time

        tasks_processed = 0
        id_batch = 0
        while tasks_processed < self.tot_task:
            k = 0
            while k in range(self.m) and job.release_time <= start_next_batch and job_i < num_jobs:
                if not job.task[task_i].is_processed():
                    j_t.append([job_i, job.task[task_i]])
                    job.task[task_i].set_processed(True)
                    tasks_processed += 1
                    task_i += 1
                    if self.jobs[job_i].is_completed():
                        job.last_batch = id_batch
                        job_i += 1
                        task_i = 0
                        job = self.jobs[job_i] if job_i < num_jobs else job
                    k += 1
            batch = Batch(id_batch, self.m, j_t, start_next_batch)
            batches.append(batch)
            start_next_batch = max(batch.end, job.release_time)
            j_t = []
            id_batch += 1

        print(f'Batches : {batches}')
        return batches
