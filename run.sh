#!/bin/bash
COMPILER=g++
BIN_NAME="life"
LINKDIRS="-L/usr/lib/"
INCDIRS="-I/usr/include/irrlicht/ -I/usr/include/python3.6m/ -I/usr/include/boost"
PLATFROM_LIBS="-lrt"

cd C &&
make CC="$COMPILER" BIN_NAME="$BIN_NAME" INCDIRS="$INCDIRS" LINKDIRS="$LINKDIRS" PlATFROM_LIBS="$PLATFORM_LIBS" && 
./"$BIN_NAME"