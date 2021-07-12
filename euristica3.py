from model.batch import Batch
from model.job import Job
from model.task import Task

# STRATEGY:
# LPT/SPT -> sceglie il task più lungo/corto quando il batch è vuoto
STRATEGY = "SPT"
# CRITERIA SORT:
# R/D/T -> ordina i job per RELEASE TIME/DUE DATE/SOMMA DURATA TASK
# (se presente più di una lettera fa la somma dei termini)
CRITERIA_SORT = "RD"


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


def sort_criteria(criteria: str):
    return lambda job: (job.release_time if "R" in criteria else 0) + (job.due_date if "D" in criteria else 0) + (
        job.sum_dur_task() if "T" in criteria else 0)


class Euristica3:
    def __init__(self, jobs: [Job], capacity_batch, tot_task):
        self.jobs = jobs
        self.m = capacity_batch
        self.tot_task = tot_task

    def start(self):
        batches = self.greedy3()
        return batches

    def greedy3(self):
        self.jobs.sort(key=sort_criteria(CRITERIA_SORT))
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
                batch.add_task(job.id, task_to_insert)
                task_to_insert.set_processed(True)
                tasks_processed += 1
                task_i += 1
                if self.jobs[job_i].is_completed():
                    job.last_batch = id_batch
                    job_i += 1
                    job = self.jobs[job_i] if job_i < num_jobs else job
                k += 1
            batches.append(batch)
            start_next_batch = max(batch.end, job.release_time)
            id_batch += 1
        print(f'Batches : {batches}')
        return batches
