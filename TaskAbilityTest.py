import time
import TaskDefine

task_id = 4
task = TaskDefine.Tasks[task_id]

print('================ Task {task_id} ================')

processes = [0]*1000
max_use = 0
for behaviour in task:
    process = behaviour['process']
    request = behaviour['request']
    if request == 'free':
        processes[process.pid] = 0
    else:
        processes[process.pid] = request
    current_use = sum(processes)
    max_use = max(max_use, current_use)
    print('Max memory use: ', max_use, end='\r')
    # time.sleep(0.01)
print('Max memory use: ', max_use, '\n')

