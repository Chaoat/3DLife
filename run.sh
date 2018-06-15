#!/bin/bash

trap "exit" INT TERM ERR
trap "kill 0" EXIT

clear
COMPILER=g++
BIN_NAME="life"
LINKDIRS="-L/usr/lib/"
INCDIRS="-I/usr/include/irrlicht/ -I/usr/include/python3.6m/ -I/usr/include/boost"
PLATFROM_LIBS="-lrt"

cd C &&
make CC="$COMPILER" BIN_NAME="$BIN_NAME" INCDIRS="$INCDIRS" LINKDIRS="$LINKDIRS" PlATFROM_LIBS="$PLATFORM_LIBS" && 
echo """Select simulation:
    1. 1D - 1 Time Dimension
    2. 1D - 20 Time Dimensions
    3. 3D - 1 Time Dimension
    4. 3D - 3 Time Dimensions
    5. 2D - 1 Time Dimension
    6. 4D - 1 Time Dimension
    7. 2D - Glider
    8. 2D Axes - 1 Time Dimension
    9. Butterfly - 1 Time Dimension
    """
read sim
cd ../Python && pipenv run python main.py $sim &
# cd ../Python && pipenv run python GUI.py &
/bin/sleep 3 &&
./"$BIN_NAME"

trap 'if [[ $? -eq 139 ]]; then echo "segfault !"; fi' CHLD

kill 0