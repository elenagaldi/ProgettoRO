import copy

from model.solution import Solution


class History:
    def __init__(self, initial_solution: Solution):
        self.current_solution = copy.deepcopy(initial_solution)
        self.current_cost = initial_solution.obj_function(count_vincoli=True)
        self.best_solution, self.best_cost = initial_solution, self.current_cost

        self.static_solution = False
        self.nochages_count = 0
        self.counter_search = 1
        self.stop = False
        self.must_perturb = False
        self.improvement = False
        self.ls_batch = True
        self.pert = None
        self.attracction_found_count = 0

        self.pert_destr_rep = 1
        self.pert_rand_task = 1
        self.pert_shuffel = 1

    def normalize_pert(self):
        totale = self.pert_shuffel + self.pert_shuffel + self.pert_rand_task

        return self.pert_shuffel / totale, self.pert_shuffel / totale, self.pert_rand_task / totale

    def stop_condition(self):
        pass

    def acceptance_test(self, next_solution, next_cost):
        pass

    def increment_counter_search(self):
        self.counter_search += 1

    def update_pert_rank(self):
        if self.pert == "destr_rep":
            self.pert_destr_rep += 1
        else:
            if self.pert == "shuffle":
                self.pert_shuffel += 1
            else:
                if self.pert == "swap":
                    self.pert_rand_task += 1
        self.pert = None
