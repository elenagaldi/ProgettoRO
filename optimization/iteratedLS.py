from random import random

from model.solution import Solution
from optimization import problemSpecificStrategies
from optimization.SA_Criteria_History import SACriteriaHistory
from optimization.history import History
from optimization.localSearch import local_search
from optimization.simulatedAnnealing import *


def stop_condition(history: History):
    return history.stop_condition()


def perturb_solution(solution: Solution, history: History):
    cost = solution.obj_function(count_vincoli=True)
    print("Perturbo soluzione:")
    norm_destr_rep, norm_shuffle, norm_rand_task = history.normalize_pert()
    r = random()
    if r <= norm_destr_rep:
        print("\tPerturbo facendo D&R")
        new_solution = problemSpecificStrategies.destroy_and_repair(solution)
        new_cost = new_solution.obj_function(count_vincoli=True)
        print(f'Destroy & repair rank: {history.pert_destr_rep} - new cost {new_cost} - init cost {cost}')
        if new_cost < cost:
            history.pert_destr_rep += 1
            print(f'Destroy & repair rank: {history.pert_destr_rep} ')
    else:
        if r <= norm_shuffle + norm_destr_rep:
            print("\tSHUFFLE")
            new_solution = problemSpecificStrategies.shuffle_batches(solution)
            new_cost = new_solution.obj_function(count_vincoli=True)
            print(f'Shuffle rank: {history.pert_shuffel} - new cost {new_cost} - init cost {cost}')
            if new_cost <= cost:
                history.pert_shuffel += 1
                print(f'Shuffle rank: {history.pert_shuffel} - new cost {new_cost} - init cost {cost}')
        else:
            print("\tPerturbo facendo swap dei task casuali")
            new_solution = problemSpecificStrategies.random_swap(solution, history)
            new_cost = new_solution.obj_function(count_vincoli=True)
            # new_solution, new_cost = simulated_annealing(solution)

            print(f'Random swap rank: {history.pert_rand_task} - new cost {new_cost} - init cost {cost}')
            if new_cost <= cost:
                history.pert_rand_task += 1
                print(f'Random swap rank: {history.pert_rand_task} - new cost {new_cost} - init cost {cost}')

    # # temp_solution = simulated_annealing(solution)
    # history.counter_search = 2
    # count_not_full_batch = solution.analyze_not_full_batch()
    # if count_not_full_batch >= 1 and history.counter_search % 7 == 0:
    #     print("\tPerturbo riempiendo batch non pieni")
    #     new_solution = problemSpecificStrategies.fill_not_full_batch(solution)
    # else:
    #     if history.counter_search % 2 == 0:
    #         print('\tRicerca con lo swap dei task:')
    #         new_solution, new_cost = swaptask_search(solution, True)
    #         print(f'\ttask local search costo : {new_cost}')
    #     else:
    #         if history.counter_search % 3 == 0:
    #             print("\tPerturbo facendo D&R")
    #             new_solution = problemSpecificStrategies.destroy_and_repair(solution)
    #         else:
    #             if history.counter_search % 5 == 0:
    #                 print("\tSHUFFLE")
    #                 new_solution = problemSpecificStrategies.shuffle_batches(solution)
    #             else:
    #                 print("\tPerturbo facendo swap dei task casuali")
    #                 new_solution = problemSpecificStrategies.random_swap(solution, history)
    return new_solution


def acceptance_test(temp_solution: Solution, temp_cost: int, history: History):
    return history.acceptance_test(temp_solution, temp_cost)


def start(initial_solution: Solution):
    history = SACriteriaHistory(initial_solution)
    current_solution, current_cost = local_search(initial_solution, neighborhood=0)
    history.best_solution, history.best_cost = current_solution, current_cost
    while stop_condition(history) is False:
        print(f'Iterated Local search: {history.counter_search}')
        temp_solution = current_solution
        if history.static_solution:
            temp_solution = perturb_solution(current_solution, history)
        count_not_full_batch = current_solution.analyze_not_full_batch()
        if count_not_full_batch >= 1:
            temp_solution = problemSpecificStrategies.fill_not_full_batch(temp_solution)
        if history.ls_batch:
            print("Batch local search:")
            temp_solution, temp_cost = simulated_annealing(temp_solution, current_cost)
            temp_solution, temp_cost = local_search(temp_solution, neighborhood=0)
            if temp_cost >= history.best_cost:
                history.ls_batch = False
        if not history.ls_batch:
            print('Applico la LS_tasks:')
            # temp_solution, temp_cost = simulated_annealing_tasks(temp_solution)
            temp_solution, temp_cost = local_search(temp_solution, neighborhood=1)
            history.ls_batch = True
        current_solution, current_cost = acceptance_test(temp_solution, temp_cost, history)
        history.increment_counter_search()
    return history.best_solution, history.best_cost
