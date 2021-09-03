import copy
from random import randrange, choice, shuffle

from model.batch import Batch
from model.job import Job
from model.solution import Solution
from model.task import Task


def list_to_dict(ll: list, count=None):
    if count is not None:
        return {k: ll[k] for k in range(count)}
    else:
        return {k: ll[k] for k in range(len(ll))}


def generate():
    njob = randrange(10, 21)
    ntask = randrange(5, 11)
    capacity = randrange(3, 6)
    nbatch = randrange(10, njob * ntask)

    batches = [Batch(i, capacity, []) for i in range(nbatch)]
    jobs = []
    for i in range(njob):
        rl = randrange(300)
        jobs.append(Job(i, rl, randrange(rl, 500), []))
    # jobs = [Job(i, randrange(100), None) for i in range(njob)]
    jobs_dict = list_to_dict(jobs, njob)
    tasks = [Task(i, randrange(1, 10)) for i in range(ntask)]

    for batch in batches:
        for i in range(randrange(1, capacity + 1)):
            batch.add_task2((randrange(njob), choice(tasks)))

    solution = Solution(batches, jobs_dict)
    solution.update_batches_start_and_end()

    # for job in solution.jobs.values():
    #     for batch in reversed(solution.batches):
    #         job_in_batch = [jobtask[0] for jobtask in batch.j_t]
    #         if job.id in job_in_batch:
    #             job.last_batch = batch.id
    #             job.due_date = batch.end
    #             break
    solution.update_solution_parameters()

    jobtask = []
    for batch in solution.batches:
        jobtask.extend(batch.j_t)
        batch.j_t.clear()

    jobtask = list(dict.fromkeys(jobtask))
    shuffle(jobtask)

    for i in range(len(jobs)):
        jobs[i].task.extend([copy.deepcopy(jt[1]) for jt in jobtask if jt[0] == jobs[i].id])

    jobs = [job for job in jobs if len(job.task) > 0]
    solution.jobs = list_to_dict(jobs, njob)
    while jobtask:
        batch = choice([b for b in solution.batches if not b.full_batch()])
        batch.add_task2(jobtask.pop(0))

    solution.delete_empty_batch()
    solution.update_solution_parameters()

    return solution, jobs
