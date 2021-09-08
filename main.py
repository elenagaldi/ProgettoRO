import configuration
from firstSolution.greedy2 import Greedy2
from firstSolution.greedy3 import Greedy3
from firstSolution.greedyBattery import greedyBattery
from inputData import randomInput
from inputData.xlsInputData import XlsInputData
from model.job import Job
from model.solution import Solution
from model.task import Task
from optimization import localSearch, iteratedVNS
from optimization.SA_Criteria_History import *
import pandas as pd


def list_to_dict(ll: list, count=None):
    if count is not None:
        return {k: ll[k] for k in range(count)}
    else:
        return {k: ll[k] for k in range(len(ll))}


def average(ll: [int]):
    s = sum(ll)
    return s / len(ll)


def generate_initial_solution(jobs, capacity_batch, tot_task, jobs_dict):
    solutions = greedyBattery(jobs, capacity_batch, tot_task, jobs_dict)
    costi_iniziali = []
    for pos, sol in enumerate(solutions):
        sol.id = pos
        costi_iniziali.append(sol.cost)
        if sol.cost == 0:
            return sol
        print(f'Soluzione {pos} -> Costo: {sol.cost}, greedy: {sol.greedy}')

    # solution.analyze_solution()

    solutions = list(filter(lambda sl: sl.cost <= average(costi_iniziali), solutions))
    # solutions.sort(key=lambda s: s.cost)
    # solutions = solutions[:4]

    best_solution = None
    best_cost = None
    for pos, sol in enumerate(solutions):
        print(f'Miglioro soluzione {sol.id}')
        sol = local_search(sol, neighborhood=0)
        if sol.cost == 0:
            return sol
        if pos == 0:
            best_solution, best_cost = sol, sol.cost
        else:
            if sol.cost < best_cost:
                best_solution, best_cost = sol, sol.cost
        print(f'Ottimo trovato: {sol.cost} \n')
    return best_solution


def mywrite_output(jl: [Job], tl: [Task], cap, solution: Solution):
    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    df = pd.DataFrame([len(jl), len(tl), cap])
    df.to_excel(writer, startcol=1, startrow=0, sheet_name='Sheet1', header=None, index=False)

    rl_list = [j.release_time for j in jl]
    dd_list = [d.due_date for d in jl]
    df_jobs = pd.DataFrame({'ReleaseTime': rl_list, 'DueDate': dd_list})
    df_jobs.to_excel(writer, sheet_name='Job', index=True)

    td_list = [t.duration for t in tl]
    df_task = pd.DataFrame({'TaskDuration': td_list})
    df_task.to_excel(writer, sheet_name='Task', index=True)

    matrix = []
    for t in tasks:
        jt = [int(t.id in [tt.id for tt in j.task]) for j in jobs]
        matrix.append((f'task{t.id}', jt))
    df_matrix = pd.DataFrame({key: value for (key, value) in matrix})
    df_matrix.to_excel(writer, sheet_name='MatriceJ-T', index=True)

    ncosti = len(solution.cost_info)
    df_cost = pd.DataFrame({'Iterazione': [x for x in range(ncosti)],
                            'Costi': solution.cost_info})
    df_cost.to_excel(writer, sheet_name='Costi', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Costi']
    chart = workbook.add_chart({'type': 'scatter',
                                'subtype': 'smooth_with_markers'})
    chart.add_series({
        'name': '=Costi!$B$1',
        'categories': f'=Costi!$A$2:$A${ncosti + 1}',
        'values': f'=Costi!$B$2:$B${ncosti + 1}',
    })

    # Add a chart title and some axis labels.
    chart.set_title({'name': 'Variazioni costo'})
    chart.set_x_axis({'name': 'Iterazioni'})
    chart.set_y_axis({'name': 'Costo'})

    # Set an Excel chart style.
    chart.set_style(14)

    # Insert the chart into the worksheet (with an offset).
    worksheet.insert_chart('D5', chart, {'x_offset': 25, 'y_offset': 10})
    writer.save()


if __name__ == '__main__':

    input_obj = XlsInputData(configuration.INPUT_FILE9)
    jobs, jobs_num, task_num, capacity_batch, durate_task_l = input_obj.read_jobs()
    jobs_dict: dict = list_to_dict(jobs, jobs_num)
    tasks = []
    tasks = [t for j in jobs for t in j.task if t not in tasks]

    # initial_solution, jobs, tasks = randomInput.generate()
    # capacity_batch = initial_solution.batches[0].capacity
    # jobs_dict = copy.deepcopy(initial_solution.jobs)
    # jobs_num = len(jobs_dict)

    tot_task = 0  # numero dei task totali
    for i in jobs:
        tot_task += len(i.task)

    # BATTERIA GREEDY
    initial_solution = generate_initial_solution(jobs, capacity_batch, tot_task, jobs_dict)

    print(f'Migliore soluzione: {initial_solution.id}:\n{initial_solution.batches} Costo: {initial_solution.cost}')
    # best_solution.analyze_solution()
    final_solution = iteratedVNS.start(initial_solution)
    print(f'Soluzione: dopo ottimizzazione \n{final_solution.batches} Costo: {final_solution.cost}')
    # final_solution.analyze_solution()
    mywrite_output(jobs, tasks, capacity_batch, final_solution)
