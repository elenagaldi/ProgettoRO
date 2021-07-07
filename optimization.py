class Optimization:
    def __init__(self, initial_solution):
        self._solution = initial_solution

    def swap_move(self, batch_i, batch_j, job_i, task_i, job_j, task_j):
        batch1 = self._solution[batch_i]
        batch2 = self._solution[batch_j]
        batch1.remove_task(job_i, task_j)
        batch2.remove_task(job_j, task_j)
        batch1.add_task(job_j, task_j)
        batch2.add_task(job_i, task_i)

    def localsearch(self):


    def tabu_search(self):
