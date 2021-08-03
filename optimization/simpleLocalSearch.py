import copy
from model.solution import Solution


def search(solution: Solution):
    new_solution = copy.deepcopy(solution)
    cost = solution.obj_function(count_vincoli=True)
    best_solution, best_cost = solution, cost
    for pos1, batch1 in enumerate(solution.batches):
        for pos2, batch2 in enumerate(solution.batches[batch1.id + 1:], start=pos1 + 1):  # qui si pensa che i batches siano ordinati ma dopo il primo switch il batch.id non corrisponde più alla sua posizione nella lista
            new_solution.swap_batches(batch1, batch2, pos1, pos2)
            new_cost = new_solution.obj_function(count_vincoli=True)
            if new_cost < cost:
                best_cost, best_solution = new_cost, copy.deepcopy(new_solution)
            new_solution = copy.deepcopy(solution)
    return best_cost, best_solution
