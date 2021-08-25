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


def list_to_dict(ll: list, count=None):
    if count is not None:
        return {k: ll[k] for k in range(count)}
    else:
        return {k: ll[k] for k in range(len(ll))}


if __name__ == '__main__':

    input_obj = XlsInputData(configuration.INPUT_FILE13)
    jobs, jobs_num, task_num, capacity_batch, durate_task_l = input_obj.read_jobs()

    jobs_dict: dict = list_to_dict(jobs, jobs_num)
    durate_task_dict: dict = list_to_dict(durate_task_l, task_num)

    tot_task = 0  # numero dei task totali = numero variabili
    for i in jobs:
        tot_task += len(i.task)

    solutions = greedyBattery(jobs, capacity_batch, tot_task, jobs_dict)

    costi_iniziali = []
    for pos, sol in enumerate(solutions):
        initial_cost = sol.obj_function(count_vincoli=True)
        costi_iniziali.append(initial_cost)
        print(f'Soluzione {pos} -> Costo: {initial_cost}')

    print(len(solutions))

    best_solution = None
    best_cost = None
    costi = []
    for pos, sol in enumerate(solutions):
        print(f'Miglioro soluzione {pos}')
        sol, _ = local_search(sol, neighborhood=0)
        solution, cost = local_search(sol, neighborhood=1)
        costi.append(cost)
        if pos == 0:
            best_solution, best_cost = solution, cost
        else:
            if cost < best_cost:
                best_solution, best_cost = solution, cost
        print(f'Ottimo trovato: {cost} \n')

    print(costi_iniziali)
    print(costi)
    print(f'Migliore soluzione:\n{best_solution.batches} Costo: {best_cost}')

    final_solution, final_cost = iteratedVNS.start(best_solution)
    print(f'Soluzione: dopo ottimizzazione \n{final_solution.batches} Costo: {final_cost}')
    # solution.analyze_solution()
