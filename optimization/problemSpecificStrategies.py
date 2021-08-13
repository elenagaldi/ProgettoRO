from model.solution import Solution
import copy
from random import randrange, choice, shuffle

from optimization.history import History


def fill_not_full_batch(solution: Solution):
    new_solution = copy.deepcopy(solution)
    result = False
    batches_to_fill = new_solution.find_not_full_batch()

    if batches_to_fill:

        print("\tTrovati batch non pieni")

        temp_jobs: dict = copy.deepcopy(new_solution.jobs)
        batch_in = choice(batches_to_fill)

        step = randrange(2)
        if step == 0:
            print("\t\tSposto task dal job più in ritardo in un batch non pieno:")
            batch_from, jobtask_to_move = new_solution.find_latest_jobtask(temp_jobs)
            job_id, task_id = jobtask_to_move[0], jobtask_to_move[1].id
            while not (batch_from.id >= batch_in.id and temp_jobs[job_id].release_time < batch_in.start
                    # and task_extend_the_batch(jobtask_to_move[1], batch_in)
            ):
                del temp_jobs[job_id]
                if not temp_jobs:
                    break
                batch_from, jobtask_to_move = new_solution.find_latest_jobtask(temp_jobs)
                job_id, task_id = jobtask_to_move[0], jobtask_to_move[1].id
        else:

            print("\t\tSposto task casuale in un batch non pieno:")
            batch_from, jobtask_to_move = new_solution.get_random_jobtask()
            job_id, task_id = jobtask_to_move[0], jobtask_to_move[1].id

        if temp_jobs:
            print(
                f'\t\tSposto task: {(job_id, task_id)} dal batch {batch_from.id} al batch {batch_in.id}')
            new_solution.move_task_in_other_batch(batch_in.id, batch_from.id, jobtask_to_move)
            result = True
        else:
            print(f'\t\tNessun task trovato compatibile con il batch:{batch_in}')

        del temp_jobs
    else:
        print('\tNessun batch non pieno')
    return result, new_solution


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
            print(
                f'\t\t Swap tra task {(job1, task1.id)} nel batch {batch1.id} e task {(job2, task2.id)} nel batch {batch2.id}')
            new_solution.swap_task(batch1.id, batch2.id, job1, task1, job2, task2)
        else:
            print(f'\tSwap casuale tra batch ({batch1.id},{batch2.id}')
            new_solution.swap_batches(batch1, batch2, batch1.id, batch2.id)
    return new_solution


def task_extend_the_batch(task_to_move, batch_in):
    longest_jt = max(batch_in.j_t, key=lambda jt: jt[1].duration)
    return task_to_move.duration > longest_jt[1].duration


def shuffle_batches(solution: Solution):
    new_solution = copy.deepcopy(solution)
    shuffle(new_solution.batches)
    new_solution.update_solution_parameters()
    return new_solution
