from model.solution import Solution
from optimization.localSearch import local_search


def stop_condition():
    return False


def perturb_solution(solution: Solution):
    # destroy and reparid
    return solution


def start(initial_solution: Solution):
    solution, cost = local_search(initial_solution, best_improvement_strategy=True)
    while stop_condition() is False:
        temp_solution, temp_cost = local_search(perturb_solution(solution), True)
