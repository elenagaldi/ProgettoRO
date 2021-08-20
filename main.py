import configuration
from firstSolution.greedy import Greedy
from firstSolution.greedy2 import Greedy2
from firstSolution.greedy3 import Greedy3
from inputData.xlsInputData import XlsInputData
from model.solution import Solution
from optimization import localSearch, iteratedLS
from optimization.acceptanceCriteria import *
from optimization import problemSpecificStrategies


def list_to_dict(ll: list, count=None):
    if count is not None:
        return {k: ll[k] for k in range(count)}
    else:
        return {k: ll[k] for k in range(len(ll))}


if __name__ == '__main__':

    input_obj = XlsInputData(configuration.INPUT_FILE9)
    jobs, jobs_num, task_num, capacity_batch, durate_task_l = input_obj.read_jobs()

    jobs_dict: dict = list_to_dict(jobs, jobs_num)
    durate_task_dict: dict = list_to_dict(durate_task_l, task_num)

    tot_task = 0  # numero dei task totali = numero variabili
    for i in jobs:
        tot_task += len(i.task)

    greedy = Greedy3(jobs, capacity_batch, tot_task)
    batches = greedy.start()
    initial_solution = Solution(batches, jobs_dict)

    initial_solution.update_jobs_delay()
    # print(initial_solution.jobs)
    initial_cost = initial_solution.obj_function(count_vincoli=False)
    print(f'Costo:\n {initial_cost}')

    solution, cost = iteratedLS.start(initial_solution)
    print(solution.batches, f'Ottimo trovato con ILS: {cost} \n')

    solution.analyze_solution()

    '''
    for i in range(input.k):
        print(t[i].duration, " ", t[i].state)
    
    
    for i in range(input.k):
        print(j.task[i].duration, " ", j.task[i].state)
    '''

    '''
    model = LpProblem("Lab_analisi", LpMinimize)
    
    # creao l'array delle variabili che corrispondono alla fine del job
    end_job = np.array(range(input.n))
    cost = np.array(range(input.n))
    
    for i in range(input.n):
        end_job[i] = pulp.LpVariable("x", lowBound=0)
    for i in range(input.n):
        cost[i] = pulp.LpVariable("c", lowBound=0)
    
        model += sum(cost) # x + c
    for i in range(input.n):
        model += cost[i] == input.due_date[i] - end_job[i]
    
    '''
