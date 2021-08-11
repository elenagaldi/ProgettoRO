import copy
import math
from random import uniform, random, choice, sample

from model.solution import Solution
from optimization.localSearch import *
from random import *


def simulated_annealing(solution: Solution):
    TEMP_EQ = 10
    current_solution = copy.deepcopy(solution)
    current_cost = solution.obj_function(count_vincoli=True)
    best_solution, best_cost = solution, current_cost
    t = 0.2 * current_cost

    while t > 0.00001:
        for k in range(TEMP_EQ):  # imposto il ciclo fino al raggiungimento dell'equilibrio
            next_solution = copy.deepcopy(current_solution)
            batch1 = choice(next_solution.batches)
            pos1 = batch1.id
            batch2 = choice(next_solution.batches)
            while batch2.id == batch1.id:
                batch2 = choice(next_solution.batches)
            pos2 = batch2.id

            next_solution.swap_batches(batch1, batch2, pos1, pos2)
            next_cost = next_solution.obj_function(count_vincoli=True)

            # next_cost, next_solution = search_with_worsening(next_solution)
            print(f'\tSwap casuale ({pos1},{pos2}) -> Costo: {next_cost}', end=' ')
            deltaE = next_cost - current_cost
            if deltaE < 0:  # è stato ottenuto un miglioramento quindi accetto la soluzione trovata
                current_solution = copy.deepcopy(next_solution)
                current_cost = next_cost
                print(f'miglioramento', end=' ')
                if next_cost < best_cost:
                    best_solution = next_solution
                    best_cost = next_cost
                    print('globale')
                else:
                    print('')
            else:
                stato = 'invariata' if deltaE == 0 else 'peggioramento'
                print(stato, end=' ')

                r = random()
                if r < math.exp(-(deltaE / t)):
                    current_solution = copy.deepcopy(next_solution)
                    current_cost = next_cost
                    print('soluzione accettata')
                else:
                    print("soluzione rifiutata")

        t = t / 2  # abbasso la temperatura

    return best_solution, best_cost


class SimulatedAnnealing:
    def __init__(self, initial_solution: Solution, temp_eq=2, max_t=1):
        self.TEMP_EQ = temp_eq
        self.MAX_T = max_t
        self.current_solution = copy.deepcopy(initial_solution)
        self.current_cost = initial_solution.obj_function(count_vincoli=True)
        self.best_solution, self.best_cost = initial_solution, self.current_cost
        self.t = 0.2 * self.current_cost
        self.k = 0

    def stop_condition(self):
        return self.t <= self.MAX_T

    def acceptance_test(self, next_solution, next_cost):
        deltaE = next_cost - self.current_cost
        if deltaE < 0:
            self.current_solution = next_solution
            self.current_cost = next_cost
            if next_cost < self.best_cost:
                self.best_solution = next_solution
                self.best_cost = next_cost
        else:
            r = random()
            if r < math.exp(-(deltaE / self.t)):
                self.current_solution = next_solution
                self.current_cost = next_cost
        self.k += 1
        if self.k >= self.TEMP_EQ:
            self.k = 0
            self.t = self.t / 2

        return self.current_solution, self.current_cost
