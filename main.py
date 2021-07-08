import configuration
from euristica import Greedy
from euristica1 import Greedy1
from euristica2 import Greedy2
from euristica3 import Greedy3
from inputData.xlsInputData import XslInputData

# from pulp import *
# import panda as pd
from optimization import *

input_obj = XslInputData(configuration.INPUT_FILE)
jobs: [Job] = input_obj.read_jobs()
capacity_batch = input_obj.read_capacity_batch()

# print(jobs)

# t = []
# for i in range(input_obj.tasks_num):
#    t.append(Task(i, i + 2, False))

tot_task = 0  # numero dei task totali = numero variabili
for i in jobs:
    tot_task += len(i.task)

lista_task = []
for i in jobs:
    for j in range(len(i.task)):
        lista_task.append([i.id, i.release_time, i.task[j]])

greedy2 = Greedy2(jobs, lista_task, capacity_batch)
batches = greedy2.start()
#greedy = Greedy3(jobs, capacity_batch, tot_task)
#batches = greedy.start()

print(f'Costo: {obj_function(jobs, batches)}')

cost = 0
for i in range(10):  # faccio ricerca locale 10 volte
    cost, batches = localsearch(batches, jobs)

print(batches, f'Ottimo locale trovato : {cost}')

# j = Job(1, 1, 3, t)
#
# b = Batch(capacity_batch, [[j, t[0]]])
#
# print("batch", b.j_t[0][1])
#
# b.add_task(j, t[3])
#
# b.get_max_dur()
#
# j.set_task_on(2)
# print(j.get_task(2))

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
