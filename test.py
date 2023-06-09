def test_score():
    import TaskDefine
    from AllocationAPI import MemoryAllocator
    from MemoryManagement import MemoryManager

    tasks = TaskDefine.Tasks
    all_error_count = 0
    for task in tasks:
        error_count = 0
        allocator = MemoryAllocator(TaskDefine.memory_size)
        model = MemoryManager(allocator)
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
        all_error_count += error_count
    assert all_error_count == 0
