import math
from optimization.history import History
from optimization.localSearch import *
from random import *


class SACriteriaHistory(History):
    def __init__(self, initial_solution: Solution, temp_eq=5, min_t=0.1):
        super().__init__(initial_solution)
        self.TEMP_EQ = temp_eq
        self.MIN_T = min_t
        self.t = 0.2 * self.current_cost
        self.k = 0

    def stop_condition(self):
        if self.stop:
            return True
        if self.current_cost == 0:
            print("Trovato ottimo globale = 0")
            return True
        if self.attracction_found_count >= 2:
            print("Trovato bacino di attrazione 2 volte, mi fermo")
            return True
        if self.t <= self.MIN_T and self.improvement is False:
            print("Raggiunta temperatura di raffreddamento, mi fermo")
            return True
        return False

    def acceptance_test(self, next_solution: Solution, next_cost):
        if next_cost == self.best_cost:
            self.attracction_found_count += 1
        if next_solution == self.current_solution:
            print("La soluzione non è cambiata")
            self.nochages_count += 1
            self.must_perturb = True
        else:
            self.nochages_count = 0

            print(f'\tTest di accettazione: nuovo costo: {next_cost}', end=' ')
            deltaE = next_cost - self.current_cost
            if deltaE < 0:
                self.improvement = True
                self.current_solution = next_solution
                self.current_cost = next_cost
                print(f'miglioramento', end=' ')
                self.update_pert_rank()
                if next_cost < self.best_cost:
                    self.best_solution = next_solution
                    self.best_cost = next_cost
                    self.attracction_found_count = 0
                    print('globale')
                else:

                    print('')
            else:
                self.improvement = False
                stato = 'invariata' if deltaE == 0 else 'peggioramento'
                print(stato, end=' ')
                r = random()
                if r < math.exp((-deltaE / self.t)):
                    self.current_solution = next_solution
                    self.current_cost = next_cost
                    print("soluzione accettata")
                    self.update_pert_rank()
                else:
                    print("soluzione rifiutata")
                    self.must_perturb = True
            self.k += 1
            if self.k >= self.TEMP_EQ:
                self.k = 0
                self.t = self.t / 2

        return self.current_solution, self.current_cost
