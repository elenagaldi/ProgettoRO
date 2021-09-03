import copy

from firstSolution.greedy2 import Greedy2
from firstSolution.greedy3 import Greedy3
from model.solution import Solution
from itertools import combinations


def greedyBattery(jobs, capacity_batch, tot_task, jobs_dict):
    solutions: [Solution] = []
    greedy2 = Greedy2(jobs, capacity_batch, tot_task)
    greedy3 = Greedy3(jobs, capacity_batch, tot_task)

    sol = Solution(greedy2.start(), jobs_dict)
    sol.update_solution_parameters()
    solutions.append(sol)

    x = "RDT"
    criterias = ([''.join(l) for i in range(len(x), 0, -1) for l in
                  combinations(x, i)])  # lista con tutte le combinazioni dei caratteri della stringa
    strategies = ["SPT", "LPT"]

    for crt in criterias:
        for strat in strategies:
            sol1 = Solution(greedy3.start(1, crt, strat), jobs_dict)
            sol2 = Solution(greedy3.start(2, crt, strat), jobs_dict)
            if sol1 not in solutions:
                sol1.update_solution_parameters()
                solutions.append(sol1)
            if sol2 not in solutions:
                sol2.update_solution_parameters()
                solutions.append(sol2)
    return solutions
