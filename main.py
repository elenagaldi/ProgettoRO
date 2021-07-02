from model.batch import *
from model.job import *
from model.task import *
from inputData.xlsInputData import XslInputData
from configuration import *
# from pulp import *
# import panda as pd


t = []

input_obj = XslInputData(INPUT_FILE)
jobs = input_obj.read_jobs()

print(jobs)


# for i in range(input_obj.tasks_num):
#     t.append(Task(i, i+2, False))
#
# j = Job(1, 1, 3, t)
#
# b = Batch([[j, t[0]]])
#
# print("batch", b.j_t[0][1].duration)
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