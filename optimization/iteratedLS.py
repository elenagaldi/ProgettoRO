from model.solution import Solution
from optimization.acceptanceCriteria import SimulatedAnnealing, simulated_annealing
from optimization.localSearch import local_search


def stop_condition(history):
    return history.stop_condition()


def perturb_solution(solution: Solution):
    print("Perturbo soluzione:")
    sol, _ = simulated_annealing(solution)
    return sol


def acceptance_test(temp_solution: Solution, temp_cost, history):
    return history.acceptance_test(temp_solution, temp_cost)


def start(initial_solution: Solution):
    history = SimulatedAnnealing(initial_solution)
    current_solution, current_cost, _ = local_search(initial_solution, best_improvement_strategy=True)
    i = 1
    while stop_condition(history) is False:
        print(f'Iterated Local search: {i}')
        temp_solution, temp_cost, _ = local_search(perturb_solution(current_solution), True)
        current_solution, current_cost = acceptance_test(temp_solution, temp_cost, history)
        i += 1
    return current_solution, current_cost
