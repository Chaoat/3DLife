#!/bin/sh
BIN_NAME="life"
LINKDIRS="-L/usr/lib/"
INCDIRS="-I/usr/include/irrlicht/ -I/usr/include/python3.6m/ -I/usr/include/boost"

cd C &&
make CC=g++ BIN_NAME=$BIN_NAME LINKDIRS=$LINKDIRS INCDIRS=$INCDIRS && 
./$BIN_NAME