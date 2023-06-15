import re


class MemoryManager:
    def __init__(self, allocator):
        self.allocator = allocator

    def allocate(self, process, request_size):
        memory_view = self.allocator.memory_view()

        # You need to complete the code here.

        # The input of this function contains two parameters:
        #   process -- the process requesting memory, you don't need to
        #              do anything for process, just pass it to the
        #              'self.allocator.allocate_memory' function at the
        #              end of this function.
        #   request_size -- an integer indicating how many memory blocks
        #                   this process requests.

        # The first line returns 'memory_view', a list of memory blocks.
        # If a memory block is free, the corresponding item of the list
        # will be None, otherwise the item will be the process object.

        # The total size of the memory is 256 blocks.

        # You need to decide which memory to allocate to the process based
        # on 'memory_view' and 'request_size'. When you make a decision,
        # pass the starting address of the memory (i.e. 'block_start')
        # along with 'request_size' and 'process' to the function
        # 'self.allocator.allocate_memory' (see below).

        # Memory blocks will be automatically reclaimed according to
        # the definition in the process objects.
        # Find the first block of consecutive free memory blocks with the requested size

        residue = []
        for i in range(len(memory_view)):
            if memory_view[i] is not None:
                residue_time = memory_view[i].pid + \
                    memory_view[i].duration-process.pid
                residue.append(residue_time)
            else:
                residue.append(0)

        block_enough = []
        consecutive_free_blocks = 0
        cnt = 0
        for i in range(len(memory_view)):
            if memory_view[i] is None:
                cnt += 1
                consecutive_free_blocks += 1
                if consecutive_free_blocks == request_size:
                    start = i - request_size + 1
                    if start == 1:
                        left_sub = 0
                    else:
                        left_sub = abs(residue[start-2] - process.duration)
                    if i == 255:
                        right_sub = 0
                    else:
                        right_sub = abs(
                            residue[i+1] - process.duration)
                    if i == 255:
                        block_enough.append((start, left_sub, 0))
                    elif residue[i+1] != 0:
                        block_enough.append(
                            (start, left_sub, right_sub))
                    else:
                        block_enough.append((start, left_sub, None))
                        for j in range(i+1, len(memory_view)):
                            if memory_view[j] is not None:
                                start = j - request_size
                                right_sub = abs(
                                    residue[j] - process.duration)
                                block_enough.append(
                                    (start, None, right_sub))
                                break
                    continue
            else:
                consecutive_free_blocks = 0
        block_start = None
        if len(block_enough) != 0:
            idx = -1
            residue_min = 256
            for i in range(len(block_enough)):
                if block_enough[i][1] is not None and block_enough[i][2] is not None:
                    min_sub = min(block_enough[i][1], block_enough[i][2])
                    if residue_min > min_sub:
                        residue_min = min_sub
                        idx = i
            if idx != -1:
                block_start = block_enough[idx][0]
            else:
                idx = 0
                residue_min = 256
                for i in range(len(block_enough)):
                    if block_enough[i][1] is None:
                        if residue_min > block_enough[i][2]:
                            residue_min = block_enough[i][2]
                            idx = i
                    elif block_enough[i][2] is None:
                        if residue_min > block_enough[i][1]:
                            residue_min = block_enough[i][1]
                            idx = i
                block_start = block_enough[idx][0]

        if block_start is None:
            return

        self.allocator.allocate_memory(block_start, request_size, process)
