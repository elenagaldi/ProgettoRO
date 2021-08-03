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

    def swap_batches(self, batch1: Batch, batch2: Batch, pos1: int, pos2: int):
        b1, b2 = copy.deepcopy(batch1), copy.deepcopy(batch2)
        self.batches[pos1] = b2
        self.batches[pos2] = b1
        start1 = max(self.batches[pos1 - 1].end,
                     b1.get_earliest_reltime(self.jobs)) if pos1 > 1 else b1.get_earliest_reltime(self.jobs)
        start2 = max(self.batches[pos2 - 1].end, b2.get_earliest_reltime(self.jobs))
        b1.update_time(pos1, start1)
        b2.update_time(pos2, start2)

    def swap_task(self, batch_i, batch_j, job_i, task_i, job_j, task_j):
        batch1, batch2 = self.batches[batch_i], self.batches[batch_j]
        batch1.remove_task(job_i, task_i)
        batch2.remove_task(job_j, task_j)
        batch1.add_task(job_j, task_j)
        batch2.add_task(job_i, task_i)
