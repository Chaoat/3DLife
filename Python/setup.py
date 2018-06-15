from cx_Freeze import setup, Executable
import os

base = 'win32gui'

executables = [Executable("GUI.py", base=base)]

packages = []
modules = []
options = {
    'build_exe': {

        'packages': packages,
        'includes': modules,
        "include_files": []
    },

}

setup(
    name="3DLife",
    options=options,
    version="1",
    description='test',
    executables=executables
)