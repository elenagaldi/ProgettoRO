from model.batch import Batch
import copy


class Solution:
    def __init__(self, batches: [Batch], jobs_dict: dict):
        self.batches = batches
        self.jobs = jobs_dict

    def obj_function(self, count_vincoli: bool):
        cost = 0
        for job in self.jobs.values():
            aux = self.batches[job.last_batch].end - job.due_date
            if aux > 0:
                cost += aux
            if count_vincoli:
                for batch in self.batches:
                    for jobtask in batch.j_t:
                        if self.jobs[jobtask[0]].release_time > batch.start:
                            cost += 100
        return cost

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

        # aggiorno i parametri start ed end dei batch in conseguenza allo swap
        self.update_batches()

        self.update_jobs_last_batch()

    def update_batches(self):
        for pos, batch in enumerate(self.batches):
            start = max(self.batches[pos - 1].end,
                        batch.get_earliest_reltime(self.jobs)) if pos > 0 else batch.get_earliest_reltime(self.jobs)
            batch.update_time(start)

    def update_jobs_last_batch(self):
        for job in self.jobs.values():
            for batch in reversed(self.batches):
                job_in_task = [jobtask[0] for jobtask in batch.j_t]
                if job.id in job_in_task:
                    job.last_batch = batch.id
                    break

    def swap_task(self, batch_i, batch_j, job_i, task_i, job_j, task_j):
        batch1, batch2 = self.batches[batch_i], self.batches[batch_j]
        batch1.remove_task(job_i, task_i)
        batch2.remove_task(job_j, task_j)
        batch1.add_task(job_j, task_j)
        batch2.add_task(job_i, task_i)

    def analyze_delay(self):
        pass
