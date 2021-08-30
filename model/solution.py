from model.batch import Batch
from model.task import Task
import copy
from random import choice
from bisect import bisect_left


class Solution:
    def __init__(self, batches: [Batch], jobs_dict_readonly: dict):
        self.batches = batches
        self.jobs = copy.deepcopy(jobs_dict_readonly)
        self.cost = None

    def obj_function(self, count_vincoli: bool):
        cost = 0
        for job in self.jobs.values():
            if job.delay > 0:
                cost += job.delay
            if count_vincoli:
                for batch in self.batches:
                    for jobtask in batch.j_t:
                        if self.jobs[jobtask[0]].release_time > batch.start:
                            print(f'Soluzione non ammissibile aumento costo di 100')
                            cost += 100
        return cost

    ## FUNZIONI INFORMATIVE DELLA SOLUZIONE

    def find_not_full_batch(self):
        b_list = []
        for batch in self.batches[:-1]:  # non controllo l'ultimo batch
            if batch.capacity > len(batch.j_t):
                b_list.append(batch)
        return b_list

    def find_latest_jobtask(self, jobs_temp: dict):
        latest_job = max(jobs_temp.values(), key=lambda j: j.delay)
        batch = self.batches[latest_job.last_batch]
        longest_jt = max(filter(lambda jt: jt[0] == latest_job.id, batch.j_t), key=lambda jt: jt[1].duration)
        return batch, longest_jt

    def analyze_solution(self):
        for job in self.jobs.values():
            print(f'Ritardo job {job.id}: {job.delay} -> ultimo batch: {job.last_batch} ')

        # for batch in self.batches:
        #     if batch.capacity > len(batch.j_t):
        #         print(f'Batch {batch.id} non pieno')
        #
        #     diff = batch.analyze_task_duration_diff()
        #     print(f' Differenza durate task nel batch {batch.id}: {diff}')

    def get_first_Mbatch_by_duration_differences(self, m):
        diff_l = []
        batch_l = []
        for pos, batch in enumerate(self.batches):
            diff = batch.analyze_task_duration_diff()
            i = bisect_left(diff_l, diff)
            diff_l.insert(i, diff)
            batch_l.insert(i, batch)
        return batch_l[-m:]

    def analyze_not_full_batch(self):
        count_nfb = 0
        for batch in self.batches:
            if batch.capacity > len(batch.j_t):
                count_nfb += 1
        return count_nfb

    ## MOSSE

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

    ## SPOST UN TASK IN UN ALTRO BATCH (NON PIENO)
    def move_task_in_other_batch(self, batch_to_fill: int, batch_to_dump: int, jt: [int, Task]):
        btf, btd = self.batches[batch_to_fill], self.batches[batch_to_dump]
        btd.remove_task(jt[0], jt[1])
        if btd.empty_batch():
            del self.batches[btd.id]
        btf.add_task(jt[0], jt[1])
        self.update_solution_parameters()

    ## DISTRUGGO UN BATCH E INSERISCO UNA LISTA NUOVA DI TASK
    def reset_batch_and_newInsert(self, batch_i: int, task_stack: [[int, Task]], strategy="SPT"):
        s = 0 if strategy == "SPT" else -1
        batch = self.batches[batch_i]
        batch_temp = copy.deepcopy(batch)
        for jt in batch_temp.j_t:
            batch.remove_task(jt[0], jt[1])
        del batch_temp
        for i in range(batch.capacity):
            if not task_stack:
                break
            jobtask_i = task_stack.pop(s)
            batch.add_task(jobtask_i[0], jobtask_i[1])
        self.update_solution_parameters()

    ## AGGIORNAMENTO PARAMETRI SOLUZIONE

    def update_solution_parameters(self):
        self.update_batches_start_and_end()
        self.update_jobs_delay()
        self.cost = self.obj_function(True)

    def update_batches_start_and_end(self):
        for pos, batch in enumerate(self.batches):
            batch.id = pos
            start = max(self.batches[pos - 1].end,
                        batch.get_latest_reltime(self.jobs)) if pos > 0 else batch.get_latest_reltime(self.jobs)
            batch.update_time(start)

    def update_jobs_delay(self):
        for job in self.jobs.values():
            for batch in reversed(self.batches):
                job_in_batch = [jobtask[0] for jobtask in batch.j_t]
                if job.id in job_in_batch:
                    job.last_batch = batch.id
                    job.delay = self.batches[job.last_batch].end - job.due_date
                    break

    def __eq__(self, other):
        if not isinstance(other, Solution):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.batches == other.batches
