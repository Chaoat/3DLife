import ctypes
import mmap

class TransferData(ctypes.Structure):
    def __init__(self, nCells, nDimensions):
        super().__init__()
        self.fields = [
            ('cells', ctypes.c_uint * nCells)
            ('drawMode', ctypes.c_bool)
            ('dimensions', ctypes.c_uint * nDimensions)
        ]

def Partition1DArray(Map):
    totalCells = 1
    for dimension in Map.dimensions:
        totalCells = totalCells*dimension
     TransferData(totalCells, len(Map.dimensions))