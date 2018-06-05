REM You have to put the Irrlicht.dll into the same folder as the exe. 
set COMPILER=g++
set BIN_NAME="life.exe"
set LINKDIRS="" 
set INCDIRS="-I/path/to/irrlicht/include/ -I/path/to/Python/Python36/include/ -I/path/to/boost/" 
set PLATFORM_LIBS = ""

REM make CC="%COMPILER%" BIN_NAME="%BIN_NAME%" LINKDIRS="%LINKDIRS%" INCDIRS="%INCDIRS%" PLATFORM_LIBS=%PLATFORM_LIBS% && cmd \K "%BIN_NAME%"

mingw32-make CC="%COMPILER%" BIN_NAME="%BIN_NAME%" LINKDIRS="%LINKDIRS%" INCDIRS="%INCDIRS%" && cmd \K "%BIN_NAME%"
