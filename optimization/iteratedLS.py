from model.solution import Solution
from optimization import problemSpecificStrategies
from optimization.acceptanceCriteria import SimulatedAnnealing, simulated_annealing
from optimization.history import History
from optimization.localSearch import local_search


def stop_condition(history: History):
    return history.stop_condition()


def perturb_solution(solution: Solution, history: History):
    print("Perturbo soluzione:")
    count_not_full_batch = solution.analyze_not_full_batch()
    if count_not_full_batch >= 1 and history.counter_search % 3 == 0:
        print("\tPerturbo riempiendo batch non pieni")
        result, new_solution = problemSpecificStrategies.fill_not_full_batch(solution)
    # sol, _ = simulated_annealing(solution)
    else:
        if history.counter_search % 2 == 0:
            print("\tPerturbo facendo swap dei task casuali")
            new_solution = problemSpecificStrategies.random_swap_task(solution, history)
        else:
            print("\tSHUFFLE")
            new_solution = problemSpecificStrategies.shuffle_batches(solution)
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
        temp_solution, temp_cost, _ = local_search(temp_solution, True)
        # print(temp_solution.batches, temp_cost)
        # temp_solution.analyze_solution()
        current_solution, current_cost = acceptance_test(temp_solution, temp_cost, history)
        history.increment_counter_search()
    return history.best_solution, history.best_cost
