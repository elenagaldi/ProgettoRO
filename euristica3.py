from model.batch import Batch
from model.job import Job
from model.task import Task

STRATEGY = "LPT"


def take_shortest_n_task_not_processed(tasks, n):
    tasks.sort(key=lambda t: t.duration)
    tasks2 = []
    x = 0
    while x in range(n) and x < len(tasks2):
        if not tasks[x].is_processed:
            tasks2.append(tasks[x])
        x += 1
    return tasks2


def get_similar_task(batch: Batch, task_list: [Task]):
    longest_task = batch.get_longest_task()
    simil_task = task_list[0]
    best_diff = abs(longest_task.duration - simil_task.duration)
    for task in task_list[1:]:
        new_diff = abs(longest_task.duration - task.duration)
        if new_diff < best_diff:
            best_diff = new_diff
            simil_task = task
    return simil_task


class Greedy3:
    def __init__(self, jobs: [Job], capacity_batch, tot_task):
        self.jobs = jobs
        self.m = capacity_batch
        self.tot_task = tot_task

    def start(self):
        batches = self.greedy3()
        return batches

    def labeling(self):
        self.jobs.sort(key=lambda x: (x.release_time))

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
                    j_t.append([job.id, job.task[task_i]])
                    job.task[task_i].set_processed(True)
                    tasks_processed += 1
                    task_i += 1
                    if self.jobs[job_i].is_completed():
                        job.last_batch = id_batch
                        job_i += 1
                        task_i = 0
                        job = self.jobs[job_i] if job_i < num_jobs else job
                    k += 1
                else:
                    tasks_processed += 1
                    task_i += 1
            batch = Batch(id_batch, self.m, j_t, start_next_batch)
            batches.append(batch)
            start_next_batch = max(batch.end, job.release_time)
            j_t = []
            id_batch += 1
        # commento per push
        print(f'Batches : {batches}')
        return batches

    def greedy3(self):
        self.jobs.sort(key=lambda x: (x.release_time + x.due_date + x.sum_dur_task()))
        num_jobs = len(self.jobs)
        # print(self.jobs)
        task_i = 0
        batches: [Batch] = []
        tasks_processed = 0
        id_batch = 0
        job_i = 0
        job = self.jobs[job_i]
        start_next_batch = job.release_time
        while tasks_processed < self.tot_task:
            k = 0
            batch = Batch(id_batch, self.m, [], start_next_batch)
            while k in range(self.m) and job.release_time <= start_next_batch and job_i < num_jobs:
                if not batch.empty_batch():
                    task_list_not_processed = [t for t in job.task if not t.is_processed()]
                    task_to_insert = get_similar_task(batch, task_list_not_processed)
                else:
                    if STRATEGY == "SPT":
                        task_to_insert = job.find_shortest_task_notprocessed()
                    else:
                        task_to_insert = job.find_longest_tast_notprocessed()
                if not task_to_insert.is_processed():
                    batch.add_task(job.id, task_to_insert)
                    task_to_insert.set_processed(True)
                    tasks_processed += 1
                    task_i += 1
                    if self.jobs[job_i].is_completed():
                        job.last_batch = id_batch
                        job_i += 1
                        job = self.jobs[job_i] if job_i < num_jobs else job
                    k += 1
                else:
                    tasks_processed += 1
                    task_i += 1
            batches.append(batch)
            start_next_batch = max(batch.end, job.release_time)
            id_batch += 1
        # commento per push
        print(f'Batches : {batches}')
        return batches
