from model.solution import Solution
import copy


def fill_not_full_batch(solution: Solution):
    new_solution = copy.deepcopy(solution)
    result = False
    batches_to_fill = new_solution.find_not_full_batch()
    if batches_to_fill:
        print("\tTrovati batch non pieni")
        for batch_in in batches_to_fill:
            temp_jobs: dict = copy.deepcopy(new_solution.jobs)
            batch_from, jobtask_to_move = new_solution.find_latest_jobtask(temp_jobs)
            job_id = jobtask_to_move[0]
            while not (batch_from.id > batch_in.id and temp_jobs[job_id].release_time < batch_in.start
                    # and task_extend_the_batch(jobtask_to_move[1], batch_in)
            ):
                del temp_jobs[job_id]
                if not temp_jobs:
                    break
                batch_from, jobtask_to_move = new_solution.find_latest_jobtask(temp_jobs)
                job_id = jobtask_to_move[0]
            if temp_jobs:
                print(
                    f'\t\tSposto task: {(job_id, jobtask_to_move[1].id)} dal batch {batch_from.id} al batch {batch_in.id}')
                new_solution.move_task_in_other_batch(batch_in.id, batch_from.id, jobtask_to_move)
                result = True
            else:
                print(f'\t\tNessun task trovato compatibile con il batch:{batch_in}')
        del temp_jobs
    else:
        print('\tNessun batch non pieno')
    return result, new_solution


def task_extend_the_batch(task_to_move, batch_in):
    longest_jt = max(batch_in.j_t, key=lambda jt: jt[1].duration)
    return task_to_move.duration > longest_jt[1].duration
