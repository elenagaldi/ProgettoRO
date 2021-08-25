import math
from optimization.history import History
from optimization.localSearch import *
from random import *


class SACriteriaHistory(History):
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

    def acceptance_test(self, next_solution: Solution, next_cost):
        if next_solution == self.current_solution:
            print("La soluzione non è cambiata")
            self.static_solution = True
        else:
            self.static_solution = False
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
