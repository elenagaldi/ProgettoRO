import copy

from model.batch import Batch
from model.job import Job


def obj_function(job_dict: dict, batch_l: [Batch], count_vincoli: bool):
    cost = 0
    for job in job_dict.values():
        aux = batch_l[job.last_batch].end - job.due_date
        if aux > 0:
            cost += aux
        if count_vincoli:
            for batch in batch_l:
                for jobtask in batch.j_t:
                    if job_dict[jobtask[0]].release_time > batch.start:
                        cost += 100
    return cost


def swap_move(solution: [Batch], batch_i, batch_j, job_i, task_i, job_j, task_j):
    batch1, batch2 = solution[batch_i], solution[batch_j]
    batch1.remove_task(job_i, task_i)
    batch2.remove_task(job_j, task_j)
    batch1.add_task(job_j, task_j)
    batch2.add_task(job_i, task_i)


def localsearch(solution: [Batch], jobs_dict: dict):
    new_solution = copy.deepcopy(solution)
    cost = obj_function(jobs_dict, solution, count_vincoli=True)
    best_solution, best_cost = solution, cost
    for batch in new_solution:
        for jobtask in batch.j_t:
            job, task = jobtask[0], jobtask[1]
            for batch2 in new_solution[batch.id + 1:]:
                for jobtask2 in batch2.j_t:
                    job2, task2 = jobtask2[0], jobtask2[1]
                    swap_move(new_solution, batch.id, batch2.id, job, task, job2, task2)
                    new_cost = obj_function(jobs_dict, new_solution, count_vincoli=True)
                    if new_cost < cost:
                        best_cost, best_solution = new_cost, copy.deepcopy(new_solution)
                    new_solution = copy.deepcopy(solution)
    return best_cost, best_solution


class Optimization:
    def __init__(self, initial_solution, tot_task):
        self._solution = initial_solution
        self._tot_task = tot_task

    def tabu_search(self):
        pass
