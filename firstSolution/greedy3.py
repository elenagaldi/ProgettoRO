import copy

from model.batch import Batch
from model.job import Job
from model.task import Task


# STRATEGY:
# LPT/SPT -> sceglie il task più lungo/corto quando il batch è vuoto
# STRATEGY = "SPT"
# CRITERIA SORT:
# R/D/T -> ordina i job per RELEASE TIME/DUE DATE/SOMMA DURATA TASK
# (se presente più di una lettera fa la somma dei termini)
# CRITERIA_SORT = "RDT"


def get_similar_task(batch: Batch, task_list: [(Job, Task)]):
    longest_task = batch.get_longest_task()
    simil_task = task_list[0]
    best_diff = abs(longest_task.duration - simil_task[1].duration)
    for task in task_list[1:]:
        new_diff = abs(longest_task.duration - task[1].duration)
        if new_diff < best_diff:
            best_diff = new_diff
            simil_task = task
        if best_diff == 0:
            return simil_task
    return simil_task


def average_change(ll: [int]):
    mysum = 0
    n = 0
    for x, y in zip(ll[0::1], ll[1::1]):
        mysum += abs(x - y)
        n += 1
    return round(mysum / n)


def average_change2(ll: [int]):
    mysum = 0
    n = 0
    for pos, x in enumerate(ll):
        for y in ll[pos + 1:]:
            mysum += abs(x - y)
            n += 1
    return round(mysum / n)


def sort_criteria(criteria: str):
    return lambda job: (job.release_time if "R" in criteria else 0) + (job.due_date if "D" in criteria else 0) + (
        job.sum_dur_task() if "T" in criteria else 0)


class Greedy3:
    def __init__(self, jobs: [Job], capacity_batch: int, tot_task: int):
        self.jobs = copy.deepcopy(jobs)
        self.m = capacity_batch
        self.tot_task = tot_task

    def start(self, version=1, criteria_sort: str = "RDT", strategy: str = "SPT"):
        init_jobs = copy.deepcopy(self.jobs)
        batches = self.greedy3(criteria_sort, strategy) if version == 1 else self.greedy3v2(criteria_sort, strategy)
        self.jobs = init_jobs
        return batches

    def greedy3(self, criteria_sort: str, strategy: str):
        self.jobs.sort(key=sort_criteria(criteria_sort))
        num_jobs = len(self.jobs)
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
                    task_list_not_processed = [(job, t) for t in job.task if not t.is_processed()]
                    t = get_similar_task(batch, task_list_not_processed)
                    task_to_insert = t[1]
                else:
                    if strategy == "SPT":
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
        return batches

    def greedy3v2(self, criteria_sort: str, strategy: str):
        self.jobs.sort(key=sort_criteria(criteria_sort))

        values: [int] = list(map(sort_criteria(criteria_sort), self.jobs))
        avg_change = average_change2(values)
        num_jobs = len(self.jobs)
        # print(self.jobs)
        task_i = 0
        batches: [Batch] = []
        tasks_processed = 0
        id_batch = 0
        job_i = 0
        job = self.jobs[job_i]
        max_start = job.release_time

        job_to_check = self.get_near_jobs(job_i, job, values, avg_change)
        while tasks_processed < self.tot_task:
            k = 0
            batch = Batch(id_batch, self.m, [], 0)
            while k in range(self.m) and job_i < num_jobs:
                if not self.jobs[job_i].is_completed():
                    if not batch.empty_batch():
                        task_list_not_processed = [(job, t) for job in job_to_check for t in job.task if
                                                   not t.is_processed()]

                        t = get_similar_task(batch, task_list_not_processed)
                        job_to_insert: Job = t[0]
                        task_to_insert: Task = t[1]
                    else:
                        job_to_insert = job
                        if strategy == "SPT":
                            task_to_insert = job.find_shortest_task_notprocessed()
                        else:
                            task_to_insert = job.find_longest_tast_notprocessed()
                    if job_to_insert.release_time > max_start:
                        max_start = job_to_insert.release_time
                    batch.add_task(job_to_insert.id, task_to_insert)
                    task_to_insert.set_processed(True)
                    tasks_processed += 1
                    task_i += 1
                    if job_to_insert.is_completed():
                        job_to_insert.last_batch = id_batch
                else:
                    job.last_batch = id_batch
                    job_i += 1
                    job = self.jobs[job_i] if job_i < num_jobs else job
                    if job_i < num_jobs:
                        job_to_check = self.get_near_jobs(job_i, job, values, avg_change)
                k += 1
            batch.start = max_start
            batch.end = batch.calc_end()
            batches.append(batch)
            max_start = max(batch.end, job.release_time)
            id_batch += 1
        return batches

    def get_near_jobs(self, job_i, job, values, avg_change):
        job_to_check: [Job] = [job]
        this_value = values[job_i]
        for pos, next_job in enumerate(self.jobs[job_i + 1:]):
            value = values[job_i + 1 + pos]
            if abs(value - this_value) <= avg_change:
                job_to_check.append(next_job)
            else:
                break
        return job_to_check
