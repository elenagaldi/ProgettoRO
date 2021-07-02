from openpyxl import load_workbook

# from numpy import array
# from configuration import INPUT_FILE
from model.job import Job
from model.task import Task


class XslInputData:
    def __init__(self, input_file):
        file_excel = load_workbook(input_file, data_only=True)
        print(file_excel.sheetnames)

        self.sheet1 = file_excel['Sheet1']
        self.sheet_task = file_excel['Task']
        self.sheet_matrix = file_excel['MatriceJ-T']
        self.sheet_job = file_excel['Job']
        self.jobs_num = int(self.sheet1['B1'].value)  # vado a leggere il numero di jobs
        self.tasks_num = int(self.sheet1['B2'].value)  # vado a leggere il numero di tasks
        self.capacity_batch = int(self.sheet1[
                                      'B3'].value)  # vado a leggere il numero di provette che possono essere processate contemporaneamente

    def read_jobs(self):
        # Vado a leggere la matrice Job_x_Task
        matrix_TJ = [[0] * self.tasks_num for _ in range(self.jobs_num)]
        for i in range(self.jobs_num):
            for j in range(self.tasks_num):
                matrix_TJ[i][j] = self.sheet_matrix.cell(i + 2, j + 2).value
        print(matrix_TJ)

        # Vado a leggere le durate dei task e le metto in un array
        # duration_t = array('I', range(tasks_num))
        duration_t = []
        for i in range(self.tasks_num):
            # duration_t = sheet_task.cell(i + 2, 2).value
            duration_t.append(self.sheet_task.cell(i + 2, 2).value)
        print(duration_t)

        jobs = []
        # Vado a crearmi la lista dei jobs.
        for i in range(self.jobs_num):
            list_task_job = []
            for j in range(self.tasks_num):
                list_task_job.append(
                    Task(j, matrix_TJ[i][j] * duration_t[j]))  # per ciascun jobs, vado a leggere e tenere in
                # memoria la durata dei task (la durata sarà 0 per i tasks non presenti in quello specifico jobs
            jobs.append(Job(i, self.sheet_job.cell(i + 2, 2).value, self.sheet_job.cell(i + 2, 3).value,
                            list_task_job))  # inizializzo il
            # jobs con il suo id, releaseTime, dueDate, e la lista dei suoi task e lo aggiungo alla lista dei jobs
        return jobs

    def read_capacity_batch(self):
        return self.capacity_batch
