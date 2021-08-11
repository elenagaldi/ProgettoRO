from model.batch import Batch
from model.task import Task
import copy


class Solution:
    def __init__(self, batches: [Batch], jobs_dict: dict):
        self.batches = batches
        self.jobs = jobs_dict

    def obj_function(self, count_vincoli: bool):
        cost = 0
        for job in self.jobs.values():
            if job.delay > 0:
                cost += job.delay
            if count_vincoli:
                for batch in self.batches:
                    for jobtask in batch.j_t:
                        if self.jobs[jobtask[0]].release_time > batch.start:
                            cost += 1000
        return cost

    def find_not_full_batch(self):
        b_list = []
        for batch in self.batches[:-1]:  # non controllo l'ultimo batch
            if batch.capacity > len(batch.j_t):
                b_list.append(batch)
        return b_list

    def find_latest_jobtask(self):
        latest_job = max(self.jobs.values(), key=lambda j: j.delay)
        batch = self.batches[latest_job.last_batch]
        longest_jt = max(filter(lambda jt: jt[0] == latest_job.id, batch.j_t), key=lambda jt: jt[1].duration)
        return batch, longest_jt

    def analyze_solution(self):
        for job in self.jobs.values():
            print(f'Ritardo job {job.id}: {job.delay} ')

        for batch in self.batches:
            if batch.capacity > len(batch.j_t):
                print(f'Batch {batch.id} non pieno')

            aux = 0
            weight = 1
            for jt1, jt2 in zip(batch.j_t[0::1], batch.j_t[1::1]):
                auxTemp = abs(jt1[1].duration - jt2[1].duration) * weight
                weight += 1 if auxTemp > 0 else 0
                aux = aux + auxTemp
            print(f' Differenza durate task nel batch {batch.id}: {aux}')

    # effettuo scambio tra due batch
    # batch1 passa da pos1 a pos2, batch2 passa da pos2 a pos1
    def swap_batches(self, batch1: Batch, batch2: Batch, pos1: int, pos2: int):
        ## effettuo una deepcopy per non modificare batch nella soluzione originale
        ## nel caso siano stati passati per riferimento
        b2, b1 = copy.deepcopy(batch1), copy.deepcopy(batch2)
        ## scambio i batch nella soluzione
        self.batches[pos1] = b1
        self.batches[pos2] = b2
        # aggiorno gli id dei batch
        b1.id = pos1
        b2.id = pos2
        # aggiorno i parametri dei batch e job in conseguenza allo swap
        self.update_solution_parameters()

    def swap_task(self, batch_i: int, batch_j: int, job_i: int, task_i: Task, job_j: int, task_j: Task):
        batch1, batch2 = self.batches[batch_i], self.batches[batch_j]
        batch1.remove_task(job_i, task_i)
        batch2.remove_task(job_j, task_j)
        batch1.add_task(job_j, task_j)
        batch2.add_task(job_i, task_i)
        self.update_solution_parameters()

    def update_solution_parameters(self):
        self.update_batches_start_and_end()
        self.update_jobs_delay()

    def update_batches_start_and_end(self):
        for pos, batch in enumerate(self.batches):
            start = max(self.batches[pos - 1].end,
                        batch.get_earliest_reltime(self.jobs)) if pos > 0 else batch.get_earliest_reltime(self.jobs)
            batch.update_time(start)

    def update_jobs_delay(self):
        for job in self.jobs.values():
            for batch in reversed(self.batches):
                job_in_batch = [jobtask[0] for jobtask in batch.j_t]
                if job.id in job_in_batch:
                    job.last_batch = batch.id
                    job.delay = self.batches[job.last_batch].end - job.due_date
                    break

    def move_task_in_other_batch(self, batch_to_fill: int, batch_to_dump: int, jt: [int, Task]):
        btf, btd = self.batches[batch_to_fill], self.batches[batch_to_dump]
        btd.remove_task(jt[0], jt[1])
        btf.add_task(jt[0], jt[1])
        self.update_solution_parameters()

    def __eq__(self, other):
        if not isinstance(other, Solution):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.batches == other.batches
