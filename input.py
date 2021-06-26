from openpyxl import load_workbook
from numpy import array
from configuration import INPUT_FILE

file_excel = load_workbook(INPUT_FILE, data_only=True)
print(file_excel.sheetnames)
# dal primo foglio della mia cartella excel
sheet1 = file_excel["Sheet1"]
n = sheet1['B1'].value # vado a leggere il numero di jobs
k = sheet1['B2'].value # vado a leggere il numero di tasks
M = sheet1['B3'].value # vado a leggere il numero di provette che possono essere processate contemporaneamente

# dal secondo foglio leggo i release time di ogni job
sheet2 = file_excel['ReleaseTime']
release_time = array(range(n))
for i in range(n):
    # print(i)
    release_time[i] = sheet2.cell(i+1, 1).value
print(release_time)

# dal terzo foglio leggo i duedate di ogni job
sheet3 = file_excel['DueDate']
due_date = array(range(n))
for i in range(n):
    # print(i)
    due_date[i] = sheet3.cell(i+1, 1).value
print(due_date)

# dal quarto foglio leggo la matrice Task x Job (colonne in un job che task vengono eseguiti)
sheet4 = file_excel['MatriceJ-T']
matrix_TJ = [[0]*n for _ in range(k)]

for i in range(k):
    for j in range(n):
        matrix_TJ[i][j] = sheet4.cell(i+1, j+1).value

print(matrix_TJ)

# dal quinto foglio leggo l'array delle durate dei tasks
sheet5 = file_excel['TaskDuration']
task_d = array(range(k))

for i in range(k):
    task_d[i] = sheet5.cell(i+1, 1).value

print(task_d)

'''
jobs = array(range(1, n+1))
print(jobs)

tasks = matrix_TJ * jobs
print(tasks)
'''
