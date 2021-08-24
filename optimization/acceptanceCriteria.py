import copy
import math
from random import uniform, random, choice, sample

from model.solution import Solution
from optimization.history import History
from optimization.localSearch import *
from random import *

def simulated_annealing_tasks(solution: Solution):
    TEMP_EQ = 10
    current_solution = copy.deepcopy(solution)
    current_cost = solution.obj_function(count_vincoli=True)
    best_solution, best_cost = solution, current_cost
    t = 0.2 * current_cost

    while t > 0.001:
        for k in range(TEMP_EQ):  # imposto il ciclo fino al raggiungimento dell'equilibrio
            next_solution = copy.deepcopy(current_solution)
            batch1 = choice(next_solution.batches)
            batch2 = choice(next_solution.batches)
            while batch2.id == batch1.id:
                batch2 = choice(next_solution.batches)

            jobtask1 = choice(batch1.j_t)
            job1, task1 = jobtask1[0], jobtask1[1]

            jobtask2 = choice(batch2.j_t)
            job2, task2 = jobtask2[0], jobtask2[1]

            next_solution.swap_task(batch1.id, batch2.id, job1, task1, job2, task2)

            next_cost = next_solution.obj_function(count_vincoli=True)

            deltaE = next_cost - current_cost
            if deltaE < 0:  # è stato ottenuto un miglioramento quindi accetto la soluzione trovata
                current_solution = copy.deepcopy(next_solution)
                current_cost = next_cost
                print(
                    f'\tSwap casuale batches ({batch1.id},{batch2.id}) job-tasks({job1} - {task1.id},{job2} - {task2.id}) -> Costo: {next_cost}',
                    end=' ')
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

def simulated_annealing(solution: Solution):
    TEMP_EQ = 10
    current_solution = copy.deepcopy(solution)
    current_cost = solution.obj_function(count_vincoli=True)
    best_solution, best_cost = solution, current_cost
    t = 0.2 * current_cost

    while t > 0.001:
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


class SimulatedAnnealing(History):
    def __init__(self, initial_solution: Solution, temp_eq=5, max_t=0.01):
        super().__init__(initial_solution)
        self.TEMP_EQ = temp_eq
        self.MAX_T = max_t
        self.t = 0.2 * self.current_cost
        self.k = 0

    def stop_condition(self):
        if self.static_solution:
            self.nochages_count += 1
        return self.t <= self.MAX_T or self.nochages_count > 3

    def acceptance_test(self, next_solution, next_cost):
        if next_solution == self.current_solution:
            print("La soluzione non è cambiata")
            self.static_solution = True
        else:
            print(f'\tTest di accettazione: nuovo costo: {next_cost}', end=' ')
            deltaE = next_cost - self.current_cost
            if deltaE < 0:
                self.current_solution = next_solution
                self.current_cost = next_cost
                print(f'miglioramento', end=' ')
                if next_cost < self.best_cost:
                    self.best_solution = next_solution
                    self.best_cost = next_cost
                    print('globale')
                else:
                    print('')
            else:
                stato = 'invariata' if deltaE == 0 else 'peggioramento'
                print(stato, end=' ')
                r = random()
                if r < math.exp(-(deltaE / self.t)):
                    self.current_solution = next_solution
                    self.current_cost = next_cost
                    print('soluzione accettata')
                else:
                    print("soluzione rifiutata")
            self.k += 1
            if self.k >= self.TEMP_EQ:
                self.k = 0
                self.t = self.t / 2

        return self.current_solution, self.current_cost
