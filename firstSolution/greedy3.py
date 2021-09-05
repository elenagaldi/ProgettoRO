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
    longest_task = longest_task[1]
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


def sort_criteria(criteria: str):
    return lambda job: (job.release_time if "R" in criteria else 0) + (job.due_date if "D" in criteria else 0) + (
        job.sum_dur_task() if "T" in criteria else 0)


def insert_jt(batch, job_to_insert, task_to_insert):
    batch.add_task2((job_to_insert.id, task_to_insert))
    task_to_insert.set_processed(True)
    if job_to_insert.is_completed():
        job_to_insert.last_batch = batch.id


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
                if self.jobs[job_i].is_completed():
                    job.last_batch = id_batch
                    job_i += 1
                    job = self.jobs[job_i] if job_i < num_jobs else job
                k += 1
            batch.end = batch.calc_end()
            batches.append(batch)
            start_next_batch = max(batch.end, job.release_time)
            id_batch += 1
        return batches

    def greedy3v2(self, criteria_sort: str, strategy: str):
        self.jobs.sort(key=sort_criteria(criteria_sort))

        num_jobs = len(self.jobs)
        batches: [Batch] = []
        tasks_processed = 0
        id_batch = 0
        job_i = 0
        job = self.jobs[job_i]
        start_next_batch = job.release_time

        while tasks_processed < self.tot_task:
            k = 0
            batch = Batch(id_batch, self.m, [], start_next_batch)

            while k < self.m and job_i < num_jobs:

                if not job.is_completed():

                    if not batch.empty_batch():

                        jt_in = batch.get_longest_task()
                        tasks_to_insert = [(j, t) for j in self.jobs for t in j.task if
                                           t.duration == jt_in[1].duration and not t.is_processed()
                                           and j.release_time <= batch.start]
                        if tasks_to_insert and sum([t.duration for t in job.task if not t.is_processed()]) + \
                                batch.start + jt_in[1].duration <= job.due_date:
                            tasks_to_insert.sort(key=lambda t: self.jobs[t[0].id].due_date)
                            tasks_to_insert = tasks_to_insert[:self.m - k + 1]
                            for jt in tasks_to_insert:
                                insert_jt(batch, jt[0], jt[1])
                                k += 1
                                if k == self.m:
                                    break
                            continue
                        else:
                            task_list_not_processed = [(job, t) for t in job.task if not t.is_processed()]
                            t = get_similar_task(batch, task_list_not_processed)
                            insert_jt(batch, job, t[1])
                            k += 1
                    else:
                        if strategy == "SPT":
                            task_to_insert = job.find_shortest_task_notprocessed()
                            insert_jt(batch, job, task_to_insert)
                            k += 1
                        else:
                            task_to_insert = job.find_longest_tast_notprocessed()
                            insert_jt(batch, job, task_to_insert)
                            k += 1
                if job.is_completed():
                    job_i += 1
                    if job_i < num_jobs:
                        job = self.jobs[job_i]
                    else:
                        break

            batch.end = batch.calc_end()
            batches.append(batch)
            start_next_batch = max(batch.end, job.release_time)
            id_batch += 1
            tasks_processed += k
        return batches
