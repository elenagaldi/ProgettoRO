import copy
from model.solution import Solution

# Best improvement strategy settato a false implica che verrà usata la First improvement strategy
from model.task import Task


def local_search(solution: Solution, neighborhood=0):
    initial_cost = solution.obj_function(count_vincoli=True)
    cost = initial_cost
    while True:
        if neighborhood == 0:
            new_cost, solution = search(solution, best_improvement_strategy=True)
        else:
            new_cost, solution = swaptask_search(solution, best_improvement_strategy=False)
        if new_cost >= cost:
            break
        cost = new_cost
    return solution, cost


def search(solution: Solution, best_improvement_strategy):
    new_solution = copy.deepcopy(solution)
    cost = solution.obj_function(count_vincoli=True)
    best_solution, best_cost = solution, cost
    swap = None
    for pos1, batch1 in enumerate(solution.batches):
        for pos2, batch2 in enumerate(solution.batches[batch1.id + 1:],
                                      start=pos1 + 1):
            new_solution.swap_batches(batch1, batch2, pos1, pos2)
            new_cost = new_solution.obj_function(count_vincoli=True)
            if new_cost < best_cost:
                best_cost, best_solution = new_cost, copy.deepcopy(new_solution)
                swap = (pos1, pos2)
                if best_improvement_strategy is False:
                    # print(f'\t\tMiglioramento con swap: {swap} ')
                    return best_cost, best_solution
            new_solution = copy.deepcopy(solution)

    # if swap is None:
    #     print(f"\t\tTrovato ottimo locale, costo:{best_cost}")
    # else:
    #     print(f'\t\tMiglioramento con swap: {swap} con costo {best_cost}')
    return best_cost, best_solution


def swaptask_search(solution: Solution, best_improvement_strategy):
    new_solution = copy.deepcopy(solution)
    cost = solution.obj_function(count_vincoli=True)
    best_solution, best_cost = solution, cost
    swap = None
    for batch in solution.batches:
        for jobtask in batch.j_t:
            job, task = jobtask[0], jobtask[1]
            for batch2 in solution.batches[batch.id + 1:]:
                for jobtask2 in batch2.j_t:
                    job2, task2 = jobtask2[0], jobtask2[1]
                    new_solution.swap_task(batch.id, batch2.id, job, task, job2, task2)
                    new_cost = new_solution.obj_function(count_vincoli=True)
                    if new_cost < best_cost:
                        best_cost, best_solution = new_cost, copy.deepcopy(new_solution)
                        swap = (batch.id, batch2.id, (job, task.id), (job2, task2.id))
                        if best_improvement_strategy is False:
                            # print(
                            #    f'\t\tMiglioramento con swap (B1,B2, Job-Task1, Job-Task2): {swap} con costo {best_cost}')
                            return best_cost, best_solution
                    new_solution = copy.deepcopy(solution)
    # if swap is None:
    #     print(f"\t\tTrovato ottimo locale, costo:{best_cost}")
    # else:
    #     print(f'\t\tMiglioramento con swap (B1,B2, Job-Task1, Job-Task2): {swap} con costo {best_cost}')
    return best_cost, best_solution
