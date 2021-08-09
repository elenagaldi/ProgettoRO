import copy
import math
from random import uniform, random, choice, sample

from model.solution import Solution
from optimization.localSearch import *
from random import *

TEMP_EQ = 5


def simulated_annealing(solution: Solution):
    current_solution = copy.deepcopy(solution)
    current_cost = solution.obj_function(count_vincoli=True)
    best_solution, best_cost = solution, current_cost
    t = 0.2 * current_cost

    while t > 0.1:
        for k in range(TEMP_EQ):  # imposto il ciclo fino al raggiungimento dell'equilibrio
            next_solution = copy.deepcopy(current_solution)
            batch1 = choice(solution.batches)
            pos1 = batch1.id
            batch2 = choice(solution.batches)
            pos2 = batch2.id
            next_solution.swap_batches(batch1, batch2, pos1, pos2)
            next_cost = next_solution.obj_function(count_vincoli=True)

            # next_cost, next_solution = search_with_worsening(current_solution)

            deltaE = next_cost - current_cost
            if deltaE < 0:  # è stato ottenuto un miglioramento quindi accetto la soluzione trovata
                current_solution = copy.deepcopy(next_solution)
                current_cost = next_cost
                if next_cost < best_cost:
                    best_solution = next_solution
                    best_cost = next_cost
            else:
                r = random()
                if r < math.exp(-(deltaE / t)):
                    current_solution = copy.deepcopy(next_solution)
        t = t / 2  # abbasso la temperatura


    return best_cost, best_solution
