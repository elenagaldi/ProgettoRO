import configuration
from firstSolution.greedy import Greedy
from firstSolution.greedy2 import Greedy2
from firstSolution.greedy3 import Greedy3
from firstSolution.greedyBattery import greedyBattery
from inputData.xlsInputData import XlsInputData
from model.solution import Solution
from optimization import localSearch, iteratedVNS
from optimization.SA_Criteria_History import *
from optimization import problemSpecificStrategies
from optimization.simulatedAnnealing import simulated_annealing
from statistics import stdev


def list_to_dict(ll: list, count=None):
    if count is not None:
        return {k: ll[k] for k in range(count)}
    else:
        return {k: ll[k] for k in range(len(ll))}


def average(l: [int]):
    s = sum(l)
    return s / len(l)


if __name__ == '__main__':

    input_obj = XlsInputData(configuration.INPUT_FILE12)
    jobs, jobs_num, task_num, capacity_batch, durate_task_l = input_obj.read_jobs()

    jobs_dict: dict = list_to_dict(jobs, jobs_num)
    durate_task_dict: dict = list_to_dict(durate_task_l, task_num)

    tot_task = 0  # numero dei task totali = numero variabili
    for i in jobs:
        tot_task += len(i.task)

    solutions = greedyBattery(jobs, capacity_batch, tot_task, jobs_dict)
    costi_iniziali = []
    for pos, sol in enumerate(solutions):
        costi_iniziali.append(sol.cost)
        print(f'Soluzione {pos} -> Costo: {sol.cost}')

    # FILTRO SOLUZIONI
    # solutions = list(filter(lambda sl: sl.cost < average(costi_iniziali) + stdev(costi_iniziali), solutions))
    # costi_iniziali = [sol.cost for sol in solutions]
    solutions = list(filter(lambda sl: sl.cost < average(costi_iniziali), solutions))

    best_solution = None
    best_cost = None
    costi = []
    for pos, sol in enumerate(solutions):
        print(f'Miglioro soluzione {pos}')
        sol = local_search(sol, neighborhood=0)
        if (jobs_num * task_num * capacity_batch) <= 100:
            sol = local_search(sol, neighborhood=1)
        costi.append(sol.cost)
        if pos == 0:
            best_solution, best_cost = sol, sol.cost
        else:
            if sol.cost < best_cost:
                best_solution, best_cost = sol, sol.cost
        print(f'Ottimo trovato: {sol.cost} \n')

    print(f'Migliore soluzione:\n{best_solution.batches} Costo: {best_cost}')
    # best_solution.analyze_solution()

    final_solution, final_cost = iteratedVNS.start(best_solution)
    print(f'Soluzione: dopo ottimizzazione \n{final_solution.batches} Costo: {final_cost}')
    # final_solution.analyze_solution()
