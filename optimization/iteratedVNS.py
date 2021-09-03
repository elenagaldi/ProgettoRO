from random import random, randrange

from model.solution import Solution
from optimization import perturbation
from optimization.SA_Criteria_History import SACriteriaHistory
from optimization.history import History
from optimization.localSearch import local_search, task_shaking
from optimization.simulatedAnnealing import *


def stop_condition(history: History):
    return history.stop_condition()


def perturb_solution(solution: Solution, history: History):
    cost = solution.cost
    print("\t\tPerturbo soluzione:")
    norm_destr_rep, norm_shuffle, norm_rand_task, norm_fnfb = history.normalize_pert()
    r = random()
    if r <= norm_destr_rep:
        print("\t\t\tPerturbo facendo D&R", end=' ')
        new_solution = perturbation.destroy_and_repairv3(solution)
        print(f' -> costo : {new_solution.cost}')
        history.pert = "destr_rep"
    else:
        if r <= norm_shuffle + norm_destr_rep:
            print("\t\t\tSHUFFLE", end=' ')
            new_solution = perturbation.shuffle_batches(solution)
            print(f' -> costo : {new_solution.cost}')
            history.pert = "destr_rep"
        else:
            count_not_full_batch = solution.analyze_not_full_batch()
            if r <= norm_fnfb + norm_shuffle + norm_destr_rep and count_not_full_batch >= 1:
                print("\t\tRiempio batch non pieni", end=' ')
                new_solution = perturbation.fill_not_full_batch(solution)
                print(f' -> costo : {new_solution.cost}')
                history.pert = "fnfb"
            else:
                print("\t\t\tPerturbo facendo swap dei task casuali", end=' ')
                # new_solution = problemSpecificStrategies.random_swap(solution, history)
                new_solution = perturbation.random_swap(solution)
                print(f' -> costo : {new_solution.cost}')
                history.pert = "swap"
    return new_solution


def acceptance_test(temp_solution: Solution, temp_cost: int, history: History):
    return history.acceptance_test(temp_solution, temp_cost)


def start(solution: Solution):
    initial_solution = solution
    history = SACriteriaHistory(initial_solution)
    current_solution, current_cost = initial_solution, initial_solution.cost
    history.best_solution, history.best_cost = current_solution, current_cost

    while stop_condition(history) is False:
        print(f'\tIterated Local search: {history.counter_search}')

        temp_solution = current_solution

        if history.must_perturb:
            temp_solution = perturb_solution(temp_solution, history)
            if temp_solution.cost < history.best_cost:
                history.best_solution = temp_solution
            history.must_perturb = False

        cost_before_batchLS = temp_solution.cost

        if history.ls_batch:
            print("\t\tSimulated Annealing:", end=' ')
            temp_solution = simulated_annealing(temp_solution)
            print(f' -> costo : {temp_solution.cost}')

            print("\t\tBatch local search:", end=' ')
            temp_solution = local_search(temp_solution, neighborhood=0)
            print(f' -> costo : {temp_solution.cost}')
            if temp_solution.cost >= cost_before_batchLS:
                history.ls_batch = False
            # cost_before_batchLS = temp_solution.cost

        if not history.ls_batch:
            print('\t\tTask local search:')
            # temp_solution = task_shaking(temp_solution)
            temp_solution = local_search(temp_solution, neighborhood=1)
            history.ls_batch = True

        current_solution, current_cost = acceptance_test(temp_solution, temp_solution.cost, history)
        history.increment_counter_search()
    return history.best_solution, history.best_cost
