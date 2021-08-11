from model.solution import Solution
import copy


def fill_not_full_batch(solution: Solution):
    new_solution = copy.deepcopy(solution)
    result = False
    batches_to_fill = new_solution.find_not_full_batch()
    if batches_to_fill:
        print("\tTrovati batch non pieni")
        temp_solution = copy.deepcopy(new_solution)
        for batch_in in batches_to_fill:
            batch_from, jobtask_to_move = temp_solution.find_latest_jobtask()
            job_id = jobtask_to_move[0]
            while not (batch_from.id > batch_in.id and temp_solution.jobs[job_id].release_time < batch_in.start
                    # and task_extend_the_batch(jobtask_to_move[1], batch_in)
            ):
                del temp_solution.jobs[job_id]
                if not temp_solution.jobs:
                    break
                batch_from, jobtask_to_move = temp_solution.find_latest_jobtask()
                job_id = jobtask_to_move[0]
            if temp_solution.jobs:
                print(
                    f'\t\tSposto task: {(job_id, jobtask_to_move[1].id)} dal batch {batch_from.id} al batch {batch_in.id}')
                new_solution.move_task_in_other_batch(batch_in.id, batch_from.id, jobtask_to_move)
                result = True
                temp_solution = copy.deepcopy(new_solution)
            else:
                print(f'\t\tNessun task trovato compatibile con il batch:{batch_in}')
        del temp_solution
    else:
        print('\tNessun batch non pieno')
    return result, new_solution


def task_extend_the_batch(task_to_move, batch_in):
    longest_jt = max(batch_in.j_t, key=lambda jt: jt[1].duration)
    return task_to_move.duration > longest_jt[1].duration
