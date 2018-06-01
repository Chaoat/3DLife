#!/bin/sh
cd C
make CC=g++ INCDIRS="-I/usr/include/irrlicht/ -I/usr/include/python3.6m/" && 
./life