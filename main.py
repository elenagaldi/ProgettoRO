import configuration
from firstSolution.greedy import Greedy
from firstSolution.greedy2 import Greedy2
from firstSolution.greedy3 import Greedy3
from firstSolution.greedyBattery import greedyBattery
from inputData import randomInput
from inputData.xlsInputData import XlsInputData
from model.solution import Solution
from optimization import localSearch, iteratedVNS
from optimization.SA_Criteria_History import *


def list_to_dict(ll: list, count=None):
    if count is not None:
        return {k: ll[k] for k in range(count)}
    else:
        return {k: ll[k] for k in range(len(ll))}


def average(ll: [int]):
    s = sum(ll)
    return s / len(ll)


def generate_initial_solution(jobs, capacity_batch, tot_task, jobs_dict):
    solutions = greedyBattery(jobs, capacity_batch, tot_task, jobs_dict)
    costi_iniziali = []
    for pos, sol in enumerate(solutions):
        costi_iniziali.append(sol.cost)
        print(f'Soluzione {pos} -> Costo: {sol.cost}')

    # solution.analyze_solution()

    solutions = list(filter(lambda sl: sl.cost < average(costi_iniziali), solutions))

    best_solution = None
    best_cost = None
    costi = []
    for pos, sol in enumerate(solutions):
        print(f'Miglioro soluzione {pos}')
        sol = local_search(sol, neighborhood=0)
        if pos == 0:
            best_solution, best_cost = sol, sol.cost
        else:
            if sol.cost < best_cost:
                best_solution, best_cost = sol, sol.cost
        print(f'Ottimo trovato: {sol.cost} \n')
    return best_solution


if __name__ == '__main__':

    input_obj = XlsInputData(configuration.INPUT_FILE4)
    jobs, jobs_num, task_num, capacity_batch, durate_task_l = input_obj.read_jobs()

    jobs_dict: dict = list_to_dict(jobs, jobs_num)

    # solution, jobs = randomInput.generate()
    # print(f'{solution.batches} Costo: {solution.cost}')
    # capacity_batch = solution.batches[0].capacity
    # jobs_dict = copy.deepcopy(solution.jobs)
    # jobs_num = len(jobs_dict)

    tot_task = 0  # numero dei task totali
    for i in jobs:
        tot_task += len(i.task)

    # BATTERIA GREEDY
    initial_solution = generate_initial_solution(jobs, capacity_batch, tot_task, jobs_dict)

    print(f'Migliore soluzione:\n{initial_solution.batches} Costo: {initial_solution.cost}')
    # best_solution.analyze_solution()
    final_solution, final_cost = iteratedVNS.start(initial_solution)
    print(f'Soluzione: dopo ottimizzazione \n{final_solution.batches} Costo: {final_cost}')
    # final_solution.analyze_solution()
