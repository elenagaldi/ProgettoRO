import math
from optimization.history import History
from optimization.localSearch import *
from random import *


class SACriteriaHistory(History):
    def __init__(self, initial_solution: Solution, temp_eq=15, min_t=0.1):
        super().__init__(initial_solution)
        self.TEMP_EQ = temp_eq
        self.MIN_T = min_t
        self.t = self.current_cost
        self.k = 0

    def stop_condition(self):
        if self.stop:
            return True
        else:
            if self.static_solution:
                self.nochages_count += 1
            if self.t <= self.MIN_T and self.improvement is False:
                print("Raggiunta temperatura di raffreddamento, mi fermo")
                return True
            else:
                if self.nochages_count > 2:
                    print("La soluzione non cambia, mi fermo")
                    return True
        return False

    def acceptance_test(self, next_solution: Solution, next_cost):
        if next_solution == self.current_solution:
            print("La soluzione non è cambiata")
            self.static_solution = True
        else:
            self.static_solution = False
            self.nochages_count = 0
            self.must_perturb = False

            print(f'\tTest di accettazione: nuovo costo: {next_cost}', end=' ')

            # if next_cost == self.best_cost:
            #     self.stop = True
            #     print("\tCosto uguale a quello globale, fermo ottimizzazione ")
            deltaE = next_cost - self.current_cost
            if deltaE < 0:
                self.improvement = True
                self.current_solution = next_solution
                self.current_cost = next_cost
                print(f'soluzione accettata con pert: {self.pert}')
                self.update_pert_rank()
                print(f'miglioramento', end=' ')
                if next_cost < self.best_cost:
                    self.best_solution = next_solution
                    self.best_cost = next_cost
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
                    print(f'soluzione accettata con pert: {self.pert}')
                    self.update_pert_rank()
                else:
                    print("soluzione rifiutata")
                    self.must_perturb = True
            self.k += 1
            if self.k >= self.TEMP_EQ:
                self.k = 0
                self.t = self.t / 2

        return self.current_solution, self.current_cost
