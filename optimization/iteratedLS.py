from random import random

from model.solution import Solution
from optimization import problemSpecificStrategies
from optimization.acceptanceCriteria import SimulatedAnnealing, simulated_annealing, simulated_annealing_tasks
from optimization.history import History
from optimization.localSearch import local_search, swaptask_search, task_local_search


def stop_condition(history: History):
    return history.stop_condition()


def perturb_solution(solution: Solution, history: History):
    cost = solution.obj_function(count_vincoli=True)
    print("Perturbo soluzione:")
    norm_destr_rep, norm_shuffle, norm_rand_task = history.normalize_pert()
    r = random()
    if r < norm_destr_rep:
        print("\tPerturbo facendo D&R")
        new_solution = problemSpecificStrategies.destroy_and_repair(solution)
        new_cost = new_solution.obj_function(count_vincoli=True)
        print(f'Destroy & repair rank: {history.pert_destr_rep} - new cost {new_cost} - init cost {cost}')
        if new_cost < cost:
            history.pert_destr_rep += 1
            print(f'Destroy & repair rank: {history.pert_destr_rep} ')
    else:
        if r < norm_shuffle + norm_destr_rep:
            print("\tSHUFFLE")
            new_solution = problemSpecificStrategies.shuffle_batches(solution)
            new_cost = new_solution.obj_function(count_vincoli=True)
            print(f'Shuffle rank: {history.pert_shuffel} - new cost {new_cost} - init cost {cost}')
            if new_cost <= cost:
                history.pert_shuffel += 1
                print(f'Shuffle rank: {history.pert_shuffel} - new cost {new_cost} - init cost {cost}')
        else:
            print("\tPerturbo facendo swap dei task casuali")
            # new_solution = problemSpecificStrategies.random_swap(solution, history)
            # new_cost = new_solution.obj_function(count_vincoli=True)  
            new_solution, new_cost = simulated_annealing(solution)

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
    history = SimulatedAnnealing(initial_solution)
    current_solution, current_cost, _ = local_search(initial_solution, best_improvement_strategy=True)
    history.best_solution, history.best_cost = current_solution, current_cost
    while stop_condition(history) is False:
        print(f'Iterated Local search: {history.counter_search}')
        temp_solution = perturb_solution(current_solution, history)
        temp_solution = problemSpecificStrategies.fill_not_full_batch(temp_solution)
        # temp_solution = simulated_annealing(temp_solution)
        # temp_solution = problemSpecificStrategies.shuffle_batches(temp_solution)
        # temp_solution, temp_cost = simulated_annealing_tasks(temp_solution)
        # temp_solution, temp_cost, _ = local_search(temp_solution, True)
        # temp_solution, temp_cost, _ = task_local_search(temp_solution, True)
        if history.ls_batch:
            temp_solution, temp_cost, _ = local_search(temp_solution, True)
            if temp_cost <= history.best_cost:
                history.ls_batch = False
        if not history.ls_batch:
            print('Applico la LS_tasks:')
            temp_solution, temp_cost, _ = task_local_search(temp_solution, True)
            history.ls_batch = True
        # else:
        #     temp_solution, temp_cost = simulated_annealing(temp_solution)

        # print(temp_solution.batches, temp_cost)
        # temp_solution, temp_cost = swaptask_search(current_solution, True)
        # temp_solution.analyze_solution()
        current_solution, current_cost = acceptance_test(temp_solution, temp_cost, history)
        history.increment_counter_search()
    return history.best_solution, history.best_cost
