import copy
from model.solution import Solution


# Best improvement strategy settato a false implica che verrà usata la First improvement strategy
def local_search(solution: Solution, best_improvement_strategy=True):
    initial_cost = solution.obj_function(count_vincoli=True)
    cost = initial_cost
    new_cost, solution = search(solution, best_improvement_strategy)
    numero_ricerce = 1
    while new_cost < cost:
        cost = new_cost
        new_cost, solution = search(solution, best_improvement_strategy)
        numero_ricerce += 1
    return solution, cost, numero_ricerce


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
                    return best_cost, best_solution
            new_solution = copy.deepcopy(solution)

    print(swap)
    return best_cost, best_solution


def search_with_worsening(solution: Solution):
    new_solution = copy.deepcopy(solution)
    cost = solution.obj_function(count_vincoli=True)
    
    best_cost = -1
    best_solution = None
    for pos1, batch1 in enumerate(solution.batches):
        for pos2, batch2 in enumerate(solution.batches[batch1.id + 1:],
                                      start=pos1 + 1):
            new_solution.swap_batches(batch1, batch2, pos1, pos2)
            new_cost = new_solution.obj_function(count_vincoli=True)
            if new_cost != cost and (new_cost < best_cost or best_cost == -1):
                best_cost, best_solution = new_cost, copy.deepcopy(new_solution)
            new_solution = copy.deepcopy(solution)
    return best_cost, best_solution


def swaptask_search(solution: Solution, best_improvement_strategy):
    new_solution = copy.deepcopy(solution)
    cost = solution.obj_function(count_vincoli=True)
    best_solution, best_cost = solution, cost
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

                        if best_improvement_strategy is False:
                            return best_cost, best_solution
                    new_solution = copy.deepcopy(solution)
    return best_cost, best_solution
