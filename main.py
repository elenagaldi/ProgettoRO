import configuration
from firstSolution.greedy import Greedy
from firstSolution.greedy2 import Greedy2
from firstSolution.greedy3 import Greedy3
from inputData.xlsInputData import XslInputData
from model.solution import Solution
from optimization import localSearch
from optimization.acceptanceCriteria import *


def list_to_dict(ll: list, count=None):
    if count is not None:
        return {k: ll[k] for k in range(count)}
    else:
        return {k: ll[k] for k in range(len(ll))}


if __name__ == '__main__':

    input_obj = XslInputData(configuration.INPUT_FILE)
    jobs, jobs_num, task_num, capacity_batch, durate_task_l = input_obj.read_jobs()

    jobs_dict: dict = list_to_dict(jobs, jobs_num)
    durate_task_dict: dict = list_to_dict(durate_task_l, task_num)

    tot_task = 0  # numero dei task totali = numero variabili
    for i in jobs:
        tot_task += len(i.task)

    greedy = Greedy3(jobs, capacity_batch, tot_task)
    batches = greedy.start()

    initial_solution = Solution(batches, jobs_dict)
    initial_cost = initial_solution.obj_function(count_vincoli=False)
    print(f'Costo:\n {initial_cost}')

    solution, cost, numero_ricerche = local_search(initial_solution, best_improvement_strategy=True)

    print(solution.batches,
          f'Ottimo locale trovato con ricerca locale : {cost} \n Numero scambi: {numero_ricerche - 1}')

    cost, solution = simulated_annealing(initial_solution)
    print(solution.batches, f'Ottimo locale trovato con simulated annealing : {cost}')

    '''cost = 0
    cost, batches = destroy_repair\
        (batches, jobs_dict, capacity_batch, tot_task)
    print(batches, f'Ottimo locale trovato con destroy and repair : {cost}')'''

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
