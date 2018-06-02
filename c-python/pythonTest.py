'''test of python embedding for c++ '''
import random
numstates = 4
dims      = [4, 3, 2, 2, 1, 2]
total     = 1
for dim in dims:
    total *= dim

# def get_state():
#     print("getting state")
#     arr = [random.randint(0, numstates) for _ in range(total)]
#     return arr

def get_state():
    # return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
    #         2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
    #         3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
    #         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
    #         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
    #         6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
    #         7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
    #         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
    #         9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    #         1, 2, 3, 4, 5, 6] 
    return [3, 1, 2, 3, 
            4, 5, 6, 7, 
            8, 9, 0, 1, 

            2, 3, 4, 5, 
            6, 7, 8, 9, 
            0, 1, 2, 3,

            0, 1, 2, 3, 
            4, 5, 6, 7, 
            8, 9, 0, 1, 

            2, 3, 4, 5, 
            6, 7, 8, 9, 
            0, 1, 2, 3,
            
            0, 1, 2, 3, 
            4, 5, 6, 7, 
            8, 9, 0, 1, 

            2, 3, 4, 5, 
            6, 7, 8, 9, 
            0, 1, 2, 3,

            0, 1, 2, 3, 
            4, 5, 6, 7, 
            8, 9, 0, 1, 

            2, 3, 4, 5, 
            6, 7, 8, 9, 
            0, 1, 2, 3]

def get_dimensions():
    return dims

def getLong():
    print("Python: Getting a long")
    return 1808495284987