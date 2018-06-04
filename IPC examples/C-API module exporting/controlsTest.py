import sys
import os 
file_path = os.path.realpath(__file__)
controlsPath = os.path.dirname(os.path.dirname(file_path)) + "/C/build/lib.linux-x86_64-3.6/"

print(controlsPath)

sys.path.append(controlsPath)
import controls
# help(controls)
controls.set_draw_mode(False)
