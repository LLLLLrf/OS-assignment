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

        block_start = None
        consecutive_free_blocks = 0
        best_block_size = 257
        state = 0
        for i, block in enumerate(memory_view):
            if block is None:
                state = 1
                consecutive_free_blocks += 1
            elif state == 1:
                state = 0
                if best_block_size > consecutive_free_blocks and consecutive_free_blocks >= request_size:
                    best_block_size = consecutive_free_blocks
                    block_start = i - consecutive_free_blocks
                consecutive_free_blocks = 0
            if block_start is None and consecutive_free_blocks >= request_size:
                block_start = i - consecutive_free_blocks + 1
        if block_start is None:
            move_state = 0
            move_start = 0
            free_cnt = 0
            i = 0
            while i < len(memory_view):
                block = memory_view[i]
                if move_state == 0 and block is None:
                    move_state = 1
                    move_start = i
                    free_cnt = 0
                if move_state == 1 and block is None:
                    free_cnt += 1
                if move_state == 1 and block is not None:
                    move_state = 0
                    self.allocator.free_memory(block)
                    self.allocator.allocate_memory(
                        move_start, block.block, block)
                    memory_view = self.allocator.memory_view()
                    i = move_start + block.block - 1
                if free_cnt >= request_size:
                    block_start = move_start
                    break
                i += 1
            block_start = move_start

        mem=[]
        loc=[]
        for ind in range(len(memory_view)):
            # 判断是否有连续的空闲内存块
            if memory_view[ind] is None:
                length=1
                for j in range(ind+1,len(memory_view)):
                    if memory_view[j] is None:
                        length+=1
                    if memory_view[j] is not None:
                        break
                if length>=request_size:
                    loc.append(ind)
                    mem.append(length)
        if len(mem)==0:
            # raise AssertionError('allocation failed')
            block_start=0
            print('allocation failed')
        else:
            
            block_start=loc[mem.index(min(mem))]

        
        

        
        self.allocator.allocate_memory(block_start, request_size, process)
