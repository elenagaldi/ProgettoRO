from model.batch import Batch
from model.job import Job
from model.solution import Solution
import copy
from random import randrange, choice, shuffle


def random_swap(solution: Solution):
    new_solution = copy.deepcopy(solution)
    for i in range(randrange(1, len(solution.batches) // 2)):
        batch1, batch2 = choice(new_solution.batches), choice(new_solution.batches)
        while batch2.id == batch1.id:
            batch2 = choice(new_solution.batches)

        jobtask1, jobtask2 = choice(batch1.j_t), choice(batch2.j_t)
        job1, job2 = jobtask1[0], jobtask2[0]
        task1, task2 = jobtask1[1], jobtask2[1]

        step = randrange(2)
        if step == 0:
            new_solution.swap_task(batch1.id, batch2.id, job1, task1, job2, task2)
        else:
            new_solution.swap_batches(batch1, batch2, batch1.id, batch2.id)
    return new_solution


def shuffle_batches(solution: Solution):
    new_solution = copy.deepcopy(solution)
    shuffle(new_solution.batches)
    new_solution.update_solution_parameters()
    return new_solution


def destroy_and_repair(solution: Solution):
    new_solution = copy.deepcopy(solution)
    capacity_batch = new_solution.batches[0].capacity

    batch_to_destroy = new_solution.get_first_Mbatch_by_duration_differences(capacity_batch)

    late_jobs: [Job] = list(filter(lambda j: j.delay > 0, new_solution.jobs.values()))

    for late_job in late_jobs:
        b = new_solution.batches[late_job.last_batch]
        if b not in batch_to_destroy:
            batch_to_destroy.append(b)

    jobtask = []
    for batch in batch_to_destroy:
        jobtask.extend(batch.j_t)

    jobtask.sort(key=lambda jt: jt[1].duration)
    size = len(jobtask)

    splitted_jt = []
    counter = 0
    for i in range(len(batch_to_destroy)):
        jt_sublist = []
        for k in range(capacity_batch):
            jt_sublist.append(jobtask[counter])
            counter += 1
            if counter >= size:
                break
        splitted_jt.append(jt_sublist)
        if counter >= size:
            break

    splitted_jt.sort(
        key=lambda jt_sub: sum([solution.jobs[jt[0]].release_time + solution.jobs[jt[0]].due_date for jt in jt_sub]))
    jobtask = [item for sublist in splitted_jt for item in sublist]  # flatten di splitten_jt

    # randchoice = randrange(2)
    # strategy = "SPT" if randchoice == 0 else "LPT"

    for batch in batch_to_destroy:
        # print(f'\t\tDistruggo batch: {batch.id}')
        if not jobtask:
            break
        new_solution.reset_batch_and_newInsert(batch.id, jobtask, "SPT")
    return new_solution


def destroy_and_repairv3(solution: Solution):
    new_solution: Solution = copy.deepcopy(solution)
    capacity_batch = new_solution.batches[0].capacity

    batch_to_destroy = new_solution.get_first_Mbatch_by_duration_differences(capacity_batch)

    late_jobs: [Job] = list(filter(lambda j: j.delay > 0, new_solution.jobs.values()))
    # batch_to_destroy = []
    # for i in range(randrange(1, len(solution.batches) // 2)):
    #     batch = choice(new_solution.batches)
    #     while batch in batch_to_destroy:
    #         batch = choice(new_solution.batches)
    #     batch_to_destroy.append(batch)

    for late_job in late_jobs:
        b = new_solution.batches[late_job.last_batch]
        if b not in batch_to_destroy:
            batch_to_destroy.append(b)

    jobtask = []
    for batch in batch_to_destroy:
        jobtask.extend(batch.j_t)
        batch.j_t.clear()

    new_solution.smart_reallocate(jobtask)
    new_solution.delete_empty_batch()
    new_solution.update_solution_parameters()

    return new_solution
