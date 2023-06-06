import time
import TaskDefine
from AllocationAPI import MemoryAllocator
from MemoryManagement import MemoryManager

import os
import platform

if platform.system().lower() == 'windows':
    def _clear():
        os.system('cls')
else:
    def _clear():
        os.system('clear')


display_content = []

def display_update():
    _clear()
    for c in display_content:
        print(c)
    time.sleep(0.01)

def memory_view(allocator):
    view = allocator.memory_view()
    s = ['']
    for i,c in enumerate(view):
        s.append('X' if c else ' ')
        if i % 32 == 31:
            s.append('\n')
    return '|'.join(s)


def test(tasks):
    global display_content
    for task_num, task in enumerate(tasks):
        # if task_num < 4: continue # Debug
        error_count = 0
        allocator = MemoryAllocator(TaskDefine.memory_size)
        model = MemoryManager(allocator)
        display_content.append('')
        for behaviour in task:
            process = behaviour['process']
            request = behaviour['request']
            try:
                if request == 'free':
                    allocator.free_memory(process)
                else:
                    model.allocate(process, request)
                    area = process.get_memory()
                    assert area is not None, 'allocation failed'
                    assert area[1] == request, 'allocation error'
            except AssertionError:
                error_count += 1
            display_content[-1] = f"""
================ Task {task_num+1} ================
\nAllocation Failed:     {error_count} \nScore for this task:   {max(10-error_count, 0)}\n
"""+ memory_view(allocator)
            display_update()
        time.sleep(1)

if __name__ == "__main__":
    test(TaskDefine.Tasks)