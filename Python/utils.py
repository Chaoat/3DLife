import sys
import os 

def getProjectRoot():
    file_path = os.path.realpath(__file__)
    return os.path.dirname(os.path.dirname(file_path))