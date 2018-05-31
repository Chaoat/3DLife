#!/bin/sh
cd c-python
make CC=g++ INCDIRS="-I/usr/include/python3.6m/"
./pytest