import copy
from random import choice

from model.solution import Solution

# Best improvement strategy settato a false implica che verrà usata la First improvement strategy
from model.task import Task


def local_search(solution: Solution, neighborhood=0):
    cost = solution.cost
    new_solution = solution
    while True:
        if neighborhood == 0:
            new_solution = search(new_solution, best_improvement_strategy=True)
        else:
            new_solution = swaptask_searchv2(new_solution, best_improvement_strategy=False)
            print(f'\t\t\t Trovato nuovo costo : {new_solution.cost}')
        new_cost = new_solution.cost
        if new_cost >= cost:
            break
        cost = new_cost
    return new_solution


def search(solution: Solution, best_improvement_strategy):
    new_solution = copy.deepcopy(solution)
    cost = solution.cost
    best_solution, best_cost = solution, cost
    swap = None
    for pos1, batch1 in enumerate(solution.batches):
        for pos2, batch2 in enumerate(solution.batches[batch1.id + 1:],
                                      start=pos1 + 1):
            new_solution.swap_batches(batch1, batch2, pos1, pos2)
            new_cost = new_solution.cost
            if new_cost < best_cost:
                best_cost, best_solution = new_cost, copy.deepcopy(new_solution)
                swap = (pos1, pos2)
                if best_improvement_strategy is False:
                    # print(f'\t\tMiglioramento con swap: {swap} ')
                    return best_solution
            new_solution = copy.deepcopy(solution)

    # if swap is None:
    #     print(f"\t\tTrovato ottimo locale, costo:{best_cost}")
    # else:
    #     print(f'\t\tMiglioramento con swap: {swap} con costo {best_cost}')
    return best_solution


def swaptask_search(solution: Solution, best_improvement_strategy):
    new_solution = copy.deepcopy(solution)
    init_cost = solution.cost
    best_solution, best_cost = solution, init_cost
    swap = None
    for batch in solution.batches:
        for pos, jobtask in enumerate(batch.j_t):
            job, task = jobtask[0], jobtask[1]
            if solution.jobs[job].delay > 0:
                for batch2 in solution.batches[batch.id + 1:]:
                    for pos2, jobtask2 in enumerate(batch2.j_t):
                        job2, task2 = jobtask2[0], jobtask2[1]
                        new_solution.swap_taskv2(batch.id, batch2.id, pos, pos2, job, task, job2, task2)
                        new_cost = new_solution.cost
                        if new_cost < best_cost:
                            best_cost, best_solution = new_cost, copy.deepcopy(new_solution)
                            swap = (batch.id, batch2.id, (job, task.id), (job2, task2.id))
                            if best_improvement_strategy is False:
                                # print(
                                #     f'\t\tMiglioramento con swap (B1,B2, Job-Task1, Job-Task2): {swap} con costo {best_cost}')
                                return best_solution
                        new_solution = copy.deepcopy(solution)
    # if swap is None:
    #     print(f"\t\tTrovato ottimo locale, costo:{best_cost}")
    # else:
    #     print(f'\t\tMiglioramento con swap (B1,B2, Job-Task1, Job-Task2): {swap} con costo {best_cost}')
    return best_solution


def swaptask_searchv2(solution: Solution, best_improvement_strategy):
    new_solution = copy.deepcopy(solution)
    cost = solution.cost
    best_solution, best_cost = solution, cost
    swap = None
    for batch in reversed(solution.batches):
        late_batch = list(set([j.last_batch for j in solution.jobs.values() if j.delay > 0]))
        if batch.id in late_batch:
            for pos, jobtask in enumerate(batch.j_t):
                job, task = jobtask[0], jobtask[1]
                for batch2 in reversed([b for b in solution.batches[:batch.id]
                                        if solution.jobs[job].release_time < b.end]):
                    for pos2, jobtask2 in enumerate(batch2.j_t):
                        job2, task2 = jobtask2[0], jobtask2[1]
                        new_solution.swap_taskv2(batch.id, batch2.id, pos, pos2, job, task, job2, task2)
                        new_cost = new_solution.cost
                        if new_cost < best_cost:
                            best_cost, best_solution = new_cost, copy.deepcopy(new_solution)
                            swap = (batch.id, batch2.id, (job, task.id), (job2, task2.id))
                            if best_improvement_strategy is False:
                                # print(
                                #     f'\t\tMiglioramento con swap (B1,B2, Job-Task1, Job-Task2): {swap} con costo {best_cost}')
                                return best_solution
                        new_solution = copy.deepcopy(solution)
    # if swap is None:
    #     print(f"\t\tTrovato ottimo locale, costo:{best_cost}")
    # else:
    #     print(f'\t\tMiglioramento con swap (B1,B2, Job-Task1, Job-Task2): {swap} con costo {best_cost}')
    return best_solution


def batch_shaking(solution: Solution):
    new_solution = copy.deepcopy(solution)
    batch1 = choice(new_solution.batches)
    pos1 = batch1.id
    batch2 = choice(new_solution.batches)
    while batch2.id == batch1.id:
        batch2 = choice(new_solution.batches)
    pos2 = batch2.id

    new_solution.swap_batches(batch1, batch2, pos1, pos2)
    return new_solution


def task_shaking(solution: Solution):
    new_solution = copy.deepcopy(solution)
    batch1 = choice(new_solution.batches)
    pos1 = batch1.id
    batch2 = choice(new_solution.batches)
    while batch2.id == batch1.id:
        batch2 = choice(new_solution.batches)
    pos2 = batch2.id

    jt1 = choice(batch1.j_t)
    jt2 = choice(batch2.j_t)

    new_solution.swap_task(batch1.id, batch2.id, jt1[0], jt1[1], jt2[0], jt2[1])
    return new_solution
