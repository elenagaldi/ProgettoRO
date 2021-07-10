import copy
from euristica2 import Greedy2
from euristica3 import Euristica3
from euristica import Greedy
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


def destroy_repair(solution: [Batch], jobs_dict: dict, capacity_batch, tot_task):
    new_solution = copy.deepcopy(solution)
    cost = obj_function(jobs_dict, solution, count_vincoli=True)
    best_solution, best_cost = solution, cost
    set_rt = {100}
    jobs = []
    for job in jobs_dict.values():
        set_rt.add(job.release_time)
        jobs.append(job)
    print(f'Prima soluzione: {new_solution}')
    # per ogni valore possibile di release time faccio destroy and repair
    for rt in set_rt:
        j_t_todo = []

        # destroy
        for batch in new_solution:
            if batch.start > rt:
                for jobtask in batch.j_t:
                    job, task = jobtask[0], jobtask[1]
                    if jobs_dict[job].release_time == rt:
                        batch.j_t.remove(jobtask)
                        task.set_processed(False)
                        for t in jobs_dict[job].task:
                            if t.id == task.id:
                                t.set_processed(False)
                        j_t_todo.append([job, task])
                    # print(task.processed)
        print(f'Nuova soluzione: {new_solution}')
        # repair
        task_in_batch = []
        for b in new_solution:
            task_in_batch.append(capacity_batch - len(b.j_t))
            # print(capacity_batch, len(b.j_t))
        task_processed = 0
        while task_processed < len(j_t_todo):
            for b in new_solution:
                max_durata = max([task[1].duration for task in b.j_t])
                k = task_in_batch[b.id]
                # for j in b.j_t:
                #     if j[1].duration > max_durata:
                #         max_durata = j[1].duration
                # print('max',max_durata)
                while k > 0:
                    best_jt = j_t_todo[0]
                    for j_t in j_t_todo:
                        # print(b.get_max_dur, best_jt[1].duration, j_t[1].duration)
                        if not j_t[1].processed:  # and max_durata-best_jt[1].duration > max_durata-j_t[1].duration > 0
                            best_jt = j_t
                    best_jt[1].set_processed(True)
                    b.j_t.append(best_jt)
                    task_processed += 1
                    for t in jobs_dict[best_jt[0]].task:
                        if t.id == best_jt[1].id:
                            t.set_processed(True)
                    if jobs_dict[best_jt[0]].is_completed:
                        print('sei completo?')
                        jobs_dict[best_jt[0]].last_batch = b.id
                    if k > 1:
                        k -= 1
                    else:
                        break
        new_cost = obj_function(jobs_dict, new_solution, count_vincoli=True)
        print(new_cost)
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
