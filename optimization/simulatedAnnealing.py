from random import uniform, random, choice, sample
import copy
from model.solution import Solution
import math

from optimization.localSearch import batch_shaking


def simulated_annealing(solution: Solution):
    TEMP_EQ = 10
    current_solution = copy.deepcopy(solution)
    current_cost = solution.obj_function(count_vincoli=True)
    best_solution, best_cost = solution, current_cost
    t = 0.2 * current_cost

    while t > 0.001:
        for k in range(TEMP_EQ):  # imposto il ciclo fino al raggiungimento dell'equilibrio
            next_solution = batch_shaking(current_solution)
            next_cost = next_solution.cost

            deltaE = next_cost - current_cost
            if deltaE < 0:  # è stato ottenuto un miglioramento quindi accetto la soluzione trovata
                current_solution = copy.deepcopy(next_solution)
                current_cost = next_cost
                if next_cost < best_cost:
                    best_solution = next_solution
                    best_cost = next_cost

                r = random()
                if r < math.exp((-deltaE / t)):
                    current_solution = copy.deepcopy(next_solution)
                    current_cost = next_cost

        t = t / 2  # abbasso la temperatura

    return best_solution
