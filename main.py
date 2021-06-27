# import input
# import batch
from job import *
from task import *
# from pulp import *
# import panda as pd
import numpy as np

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
t=list(range(input.n))
for i in range(input.n):
    t[i] = Task(i, False)
print(t[2].state)
j = Job(1, 3, t)
j.set_task_on(2)
print(j.get_task(2))
