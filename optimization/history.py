import copy

from model.solution import Solution
import time


class History:
    def __init__(self, initial_solution: Solution):
        self.current_solution = copy.deepcopy(initial_solution)
        self.current_cost = initial_solution.obj_function(count_vincoli=True)
        self.best_solution, self.best_cost = initial_solution, self.current_cost

        self.static_solution = False
        self.nochages_count = 0
        self.counter_search = 1
        self.must_perturb = False
        self.improvement = False
        self.ls_batch = True
        self.pert = None
        self.attracction_found_count = 0
        self.cost_l = []

        self.pert_destr_rep = 1
        self.pert_rand_task = 1
        self.pert_shuffel = 1

        self.max_running_time = 30
        self.start_time = time.time()

    def normalize_pert(self):
        totale = self.pert_shuffel + self.pert_shuffel + self.pert_rand_task

        return self.pert_shuffel / totale, self.pert_shuffel / totale, self.pert_rand_task / totale

    def stop_condition(self):
        pass

    def acceptance_test(self, next_solution, next_cost):
        pass

    def increment_counter_search(self):
        self.counter_search += 1

    def update_pert_rank(self, inc):
        if self.pert == "destr_rep":
            if not (inc < 0 and self.pert_destr_rep == 0):
                self.pert_destr_rep += inc
        else:
            if self.pert == "shuffle":
                if not (inc < 0 and self.pert_shuffel == 0):
                    self.pert_shuffel += inc
            else:
                if self.pert == "swap":
                    if not (inc < 0 and self.pert_rand_task == 0):
                        self.pert_rand_task += inc
        self.pert = None
