
memory_size = 256

class Process:
    def __init__(self, pid, block, duration):
        self.__block = block
        self.__duration = duration
        self.__pid = pid
        self.__memory = None
    
    @property
    def pid(self): return self.__pid

    @property
    def block(self): return self.__block

    @property
    def duration(self): return self.__duration

    def set_memory(self, memory_start, memory_end):
        self.__memory = (memory_start, memory_end)
    
    def get_memory(self):
        return self.__memory


class MemoryAllocator:
    def __init__(self, memory_size):
        self.__memory_blocks = [None] * memory_size
    
    def memory_view(self):
        '''return the array of the use of memory blocks.'''
        return tuple(self.__memory_blocks)

    def allocate_memory(self, block_start, length, process):
        # block_start+length+1
        for block_id in range(block_start, block_start+length):
            assert self.__memory_blocks[block_id] is None, 'tend to allocate occupied blocks'
            self.__memory_blocks[block_id] = process
            process.set_memory(block_start, length)


    def free_memory(self, process):
        assert process.get_memory() is not None, 'process should already hold memory blocks'
        block_start, length = process.get_memory()
        for block_id in range(block_start, block_start+length):
            assert self.__memory_blocks[block_id] == process, 'the orresponding memory blocks should be assigned to the process'
            self.__memory_blocks[block_id] = None