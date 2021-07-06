import configuration
from euristica import Greedy
from inputData.xlsInputData import XslInputData
from model.batch import Batch
from model.job import Job
from model.task import Task


# from pulp import *
# import panda as pd


def obj_function(job_l: [Job], batch_l: [Batch]):
    cost = 0
    for job in job_l:
        aux = batch_l[job.last_batch].end - job.due_date
        if aux > 0:
            # cost += job.due_date - batches[job.last_batch].end
            cost += aux
    return cost


input_obj = XslInputData(configuration.INPUT_FILE)
jobs: [Job] = input_obj.read_jobs()
capacity_batch = input_obj.read_capacity_batch()
duration_list = input_obj.read_duration_task()

print(jobs)

t = []
for i in range(input_obj.read_tasks_num):
    t.append(Task(i, i + 2, False))

tot_task = 0  # numero dei task totali = numero variabili
for i in jobs:
    tot_task += len(i.task)

greedy = Greedy(jobs, capacity_batch, tot_task)
batches = greedy.start()

print(f'Costo: {obj_function(jobs, batches)}')

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
