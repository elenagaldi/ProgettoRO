import input
from batch import *
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
t = []

for i in range(input.k):
    t.append(Task(i, i+2, False))

j = Job(1, 1, 3, t)

b = Batch([[j, t[0]]])

print("batch", b.j_t[0][1].duration)

b.add_task(j, t[3])

b.get_max_dur()



'''
for i in range(input.k):
    print(t[i].duration, " ", t[i].state)


for i in range(input.k):
    print(j.task[i].duration, " ", j.task[i].state)
'''

j.set_task_on(2)
print(j.get_task(2))
