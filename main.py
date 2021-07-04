import configuration
from euristica import Greedy
from inputData.xlsInputData import XslInputData
from model.job import Job
from model.task import Task

# from pulp import *
# import panda as pd


input_obj = XslInputData(configuration.INPUT_FILE)
jobs: [Job] = input_obj.read_jobs()
capacity_batch = input_obj.read_capacity_batch()

print(jobs)

t = []
for i in range(input_obj.tasks_num):
    t.append(Task(i, i + 2, False))

tot_task = 0  # numero dei task totali = numero variabili
for i in jobs:
    tot_task += len(i.task)

greedy = Greedy(jobs, capacity_batch, tot_task)
greedy.start()

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
