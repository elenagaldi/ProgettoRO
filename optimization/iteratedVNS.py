from random import random, randrange

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
    print("\t\tPerturbo soluzione:")
    norm_destr_rep, norm_shuffle, norm_rand_task = history.normalize_pert()
    r = random()

    if r <= norm_destr_rep:
        print("\t\t\tPerturbo facendo D&R")
        new_solution = problemSpecificStrategies.destroy_and_repair(solution)
        new_cost = new_solution.cost
        print(f'Destroy & repair rank: {history.pert_destr_rep} - new cost {new_cost} - init cost {cost}')
        if new_cost < cost:
            history.pert_destr_rep += 1
        print(f'Destroy & repair rank: {history.pert_destr_rep} ')
    else:
        if r <= norm_shuffle + norm_destr_rep:
            print("\t\t\tSHUFFLE")
            new_solution = problemSpecificStrategies.shuffle_batches(solution)
            new_cost = new_solution.cost
            print(f'Shuffle rank: {history.pert_shuffel} - new cost {new_cost} - init cost {cost}')
            if new_cost <= cost:
                history.pert_shuffel += 1
            print(f'Shuffle rank: {history.pert_shuffel} - new cost {new_cost} - init cost {cost}')
        else:
            print("\t\t\tPerturbo facendo swap dei task casuali")
            new_solution = problemSpecificStrategies.random_swap(solution, history)
            new_cost = new_solution.cost
            print(f'Random swap rank: {history.pert_rand_task} - new cost {new_cost} - init cost {cost}')
            if new_cost <= cost:
                history.pert_rand_task += 1
            print(f'Random swap rank: {history.pert_rand_task} - new cost {new_cost} - init cost {cost}')
    return new_solution


def acceptance_test(temp_solution: Solution, temp_cost: int, history: History):
    return history.acceptance_test(temp_solution, temp_cost)


def start(initial_solution: Solution):
    history = SACriteriaHistory(initial_solution)

    # current_solution = local_search(initial_solution, neighborhood=0)
    current_solution, current_cost = initial_solution, initial_solution.cost
    history.best_solution, history.best_cost = current_solution, current_cost

    while stop_condition(history) is False:
        print(f'\tIterated Local search: {history.counter_search}')
        temp_solution = current_solution

        if history.static_solution or history.must_perturb:
            temp_solution = perturb_solution(current_solution, history)
            history.perturb = False

        count_not_full_batch = current_solution.analyze_not_full_batch()
        if count_not_full_batch >= 1:
            temp_solution = problemSpecificStrategies.fill_not_full_batch(temp_solution)

        cost_before_LS = temp_solution.cost
        if history.ls_batch:
            print("\t\tCampionamento con SA:", end=' ')
            temp_solution = simulated_annealing(temp_solution)
            print(f' -> costo : {temp_solution.cost}')

            print("\t\tBatch local search:", end=' ')
            temp_solution = local_search(temp_solution, neighborhood=0)
            print(f' -> costo : {temp_solution.cost}')

            if temp_solution.cost >= cost_before_LS:
                history.ls_batch = False

        if not history.ls_batch:
            print('\t\tTask local search:', end=' ')
            # temp_solution, temp_cost = simulated_annealing_tasks(temp_solution)
            temp_solution = local_search(temp_solution, neighborhood=1)
            print(f' -> costo : {temp_solution.cost}')
            history.ls_batch = True

        current_solution, current_cost = acceptance_test(temp_solution, temp_solution.cost, history)
        history.increment_counter_search()
    return history.best_solution, history.best_cost
