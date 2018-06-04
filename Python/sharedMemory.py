import operator
from functools import reduce
import mmap
from ctypes import sizeof, Structure, c_uint, c_bool
import os

MAX_CELLS = 1048576 #1 MiB
MAX_DIMENSIONS = 20

class TransferData(Structure):
    _fields_ = [
        # max 20 dimensions
        ('dimensions', c_uint * MAX_DIMENSIONS),
        # max 1 MiB cells
        ('cells', c_uint * MAX_CELLS),
        ('drawMode', c_bool)
    ]


class SharedState():
    def __init__(self, dimensions):

        self.transferData = TransferData()

        if len(dimensions) > MAX_DIMENSIONS:
            raise ValueError("Cannot have more than 20 dimensions")

        self.cellsPerDimension = [1]
        for i in range(0, len(dimensions)):
            self.cellsPerDimension.append(self.cellsPerDimension[i] * dimensions[i])

        self.oneDIndices = [[] for _ in range(self.cellsPerDimension[-1])]

        for d in range(len(dimensions)):
            for c in range(self.cellsPerDimension[-1]):
                self.oneDIndices[c].append(c // self.cellsPerDimension[d] % self.cellsPerDimension[d + 1]) 

        # initialize shared mem
        # TODO: if we want to support multiple maps
        # we have to generate unique names for the
        # shared memory for each map, and pass
        # those as a parameter to the C++ code 

        memsize = sizeof(self.transferData)

        # Create new empty file to back memory map on disk
        fd = os.open('/tmp/3DLifeShmem', os.O_CREAT | os.O_TRUNC | os.O_RDWR)
        # Zero out the file to ensure it's the right size
        assert os.write(fd, b'\x00' * memsize) == memsize
        # Create the mmap instace with the following params:
        # fd: File descriptor which backs the mapping or -1 for anonymous mapping
        # length: Must in multiples of mmap.PAGESIZE (usually 4 KB)
        # flags: MAP_SHARED means other processes can share this mmap
        # prot: PROT_WRITE means this process can write to this mmap
        self.shmem = mmap.mmap(fd, memsize, mmap.MAP_SHARED, mmap.PROT_WRITE)

        # self.shmem = mmap(-1, sizeof(self.transferData), "TransferDataSHMEM")

        data = self.getData()
        for i in range(len(dimensions)):
            data.dimensions[i] = dimensions[i]
    
    def getData(self):
        return TransferData.from_buffer(self.transferData)

    def getOneDMap(self, map):
        # ret = [0 for _ in range(self.cellsPerDimension[-1])]

        # for c in range(self.cellsPerDimension[-1]):
        #     ret[c] = reduce(operator.getitem, self.oneDIndices[c], map)
        
        # return ret

        return [reduce(operator.getitem, self.oneDIndices[i], map) for i in range(self.cellsPerDimension[-1])]

    def update(self, map, drawMode:bool):
        data = self.getData()
        data.drawMode = drawMode

        oneDMap = self.getOneDMap(map)

        for i in range(len(oneDMap)):
            data.cells[i] = oneDMap[i]
