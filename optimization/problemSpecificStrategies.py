from model.batch import Batch
from model.job import Job
from model.solution import Solution
import copy
from random import randrange, choice, shuffle

from optimization import localSearch
from optimization.history import History


def fill_not_full_batch(solution: Solution):
    new_solution = copy.deepcopy(solution)
    batches_to_fill = new_solution.find_not_full_batch()
    task_to_swap = []
    b = 0
    for batch in batches_to_fill:
        # print("\tTrovati batch non pieni")
        for task in batch.j_t:
            task_to_swap.append([batch.id, task])
        # batches_to_fill[b].j_t.clear()
        b += 1

    task_to_swap.sort(key=lambda x: x[1][1].duration)
    # print(f'Tasks to swap: {task_to_swap}')
    n_tasks = len(task_to_swap)
    batches_to_fill.sort(key=lambda btc: btc.start)
    for batch in batches_to_fill:
        k = 0
        # print(f'prima: {batch.full_batch()}')
        while not batch.full_batch() and k < n_tasks:
            t = 0
            for task in task_to_swap:
                batch_from = task[0]
                jobtask_to_move = task[1]
                # print(jobtask_to_move)
                if batch.start >= new_solution.jobs[jobtask_to_move[0]].release_time and not batch.id == batch_from:
                    # print(
                    #    f'Sposto nel batch {batch.id} il task {jobtask_to_move[1].id} del job {new_solution.jobs[jobtask_to_move[0]].id} dal batch{batch_from}')
                    try:
                        new_solution.move_task_in_other_batch(batch.id, batch_from, jobtask_to_move)
                    except:
                        pass
                    # print(f'dopo {batch}')
                    del task_to_swap[t]
                    n_tasks = len(task_to_swap)
                    if batch.full_batch():
                        break
                t += 1
            k += 1
    # print(f'Soluzione perturbata: \n {new_solution.batches}')
    return new_solution

    # if batches_to_fill:
    #
    #     print("\tTrovati batch non pieni")
    #
    #     temp_jobs: dict = copy.deepcopy(new_solution.jobs)
    #     batch_in = choice(batches_to_fill)
    #
    #     step = randrange(2)
    #     if step == 0:
    #         print("\t\tSposto task dal job più in ritardo in un batch non pieno:")
    #         batch_from, jobtask_to_move = new_solution.find_latest_jobtask(temp_jobs)
    #         job_id, task_id = jobtask_to_move[0], jobtask_to_move[1].id
    #         while not (batch_from.id >= batch_in.id and temp_jobs[job_id].release_time < batch_in.start
    #                 # and task_extend_the_batch(jobtask_to_move[1], batch_in)
    #         ):
    #             del temp_jobs[job_id]
    #             if not temp_jobs:
    #                 break
    #             batch_from, jobtask_to_move = new_solution.find_latest_jobtask(temp_jobs)
    #             job_id, task_id = jobtask_to_move[0], jobtask_to_move[1].id
    #     else:
    #
    #         print("\t\tSposto task casuale in un batch non pieno:")
    #         batch_from, jobtask_to_move = new_solution.get_random_jobtask()
    #         job_id, task_id = jobtask_to_move[0], jobtask_to_move[1].id
    #
    #     if temp_jobs:
    #         print(
    #             f'\t\tSposto task: {(job_id, task_id)} dal batch {batch_from.id} al batch {batch_in.id}')
    #         new_solution.move_task_in_other_batch(batch_in.id, batch_from.id, jobtask_to_move)
    #         result = True
    #     else:
    #         print(f'\t\tNessun task trovato compatibile con il batch:{batch_in}')
    #
    #     del temp_jobs
    # else:
    #     print('\tNessun batch non pieno')
    # return result, new_solution


def random_swap(solution: Solution, history: History):
    new_solution = copy.deepcopy(solution)
    for i in range(randrange(1, 10)):
        batch1, batch2 = choice(new_solution.batches), choice(new_solution.batches)
        while batch2.id == batch1.id:
            batch2 = choice(new_solution.batches)

        jobtask1, jobtask2 = choice(batch1.j_t), choice(batch2.j_t)
        job1, job2 = jobtask1[0], jobtask2[0]
        task1, task2 = jobtask1[1], jobtask2[1]

        step = randrange(2)
        if step == 0:
            # print(
            #   f'\t\t Swap tra task {(job1, task1.id)} nel batch {batch1.id} e task {(job2, task2.id)} nel batch {batch2.id}')
            new_solution.swap_task(batch1.id, batch2.id, job1, task1, job2, task2)
        else:
            # print(f'\tSwap casuale tra batch ({batch1.id},{batch2.id}')
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

    # splitted_jt = []
    # counter = 0
    # for i in range(len(batch_to_destroy)):
    #     jt_sublist = []
    #     for k in range(capacity_batch):
    #         jt_sublist.append(jobtask[counter])
    #         counter += 1
    #         if counter >= size:
    #             break
    #     splitted_jt.append(jt_sublist)
    #     if counter >= size:
    #         break
    #
    # splitted_jt.sort(
    #     key=lambda jt_sub: sum([solution.jobs[jt[0]].release_time + solution.jobs[jt[0]].due_date for jt in jt_sub]))
    # jobtask = [item for sublist in splitted_jt for item in sublist]  # flatten di splitten_jt

    shuffle(batch_to_destroy)

    # randchoice = randrange(2)
    # strategy = "SPT" if randchoice == 0 else "LPT"

    for batch in batch_to_destroy:
        # print(f'\t\tDistruggo batch: {batch.id}')
        if not jobtask:
            break
        new_solution.reset_batch_and_newInsert(batch.id, jobtask, "SPT")
    return new_solution
