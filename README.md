3DLife
======

Building
-----------
To compile the c++ code you will need both a c++ compiler and the [project dependencies](#dependencies). Which operating system you use will determine which compilation commands you should use and where you have to point the compiler to find the [project dependencies](#dependencies).  

### Windows
1. Install a c++ compiler, eg. [mingw](http://www.mingw.org/) or [mingw-64](http://mingw-w64.org/doku.php).
2. Install [Irrlicht](http://irrlicht.sourceforge.net/). Copy Irrlicht.dll into the [./C](./C) folder.
3. Ensure you have the python-dev headers. Header files are included with the python binary on windows, eg. c:\Python36\include.
4. Install [Boost](https://www.boost.org/)
5. Open the file "run.bat". You should see a line that reads:
```shell
set INCDIRS="-I/some/path/ -I/another/path"
```
Replace the string between the double quotes with a list of directory paths corresponding to each directory on your system which contains project header files. Each item in the list should be preceded by "-I" (without the quotes) and items should be separated by spaces.
6. Build and run the program with the command:
```shell
$ C/run
```

### Linux
1. Install a c++ compiler, eg. [gcc](https://gcc.gnu.org/).
2. Install [Irrlicht](http://irrlicht.sourceforge.net/).
3. Install [Boost](https://www.boost.org/)
4. Ensure you have the python-dev headers. Some distributions include headers in the installation eg. usr/include/python3.6m, otherwise install the python-dev package for your distribution.
5. Ensure you have precompiled librt .so files (eg. /usr/lib/librt)
6. Open the file "run.sh". You should see a line that reads:
```shell
INCDIRS="-I/some/path/ -I/another/path"
```
7. Another line reads:
```shell
LINKDIRS="-L/some/path/ -L/another/path"
```
Replace the string between the double quotes with a list of directory paths corresponding to each directory on your system which contains precompiled .so files. Each item in the list should be preceeded by "-L" (without the quotes) and items should be separated by spaces.
8. Build and run the program with the command:
```shell
$ bash C/run.sh
```

Build Problems
--------------

You need three things in order to successfully compile the project:

1. A compiler, genius
2. The libraries the project depends on
3. The header files from those libraries that are included in the project.

All of these are platform-dependant. In order to tell the compiler this information, you will have to edit either [run.sh](./run.sh) (linux) or [run.bat](./run.bat) (windows). In the script you will see something similar to:

```shell
COMPILER=g++
BIN_NAME="life"
LINKDIRS="-L/usr/lib/"
INCDIRS="-I/usr/include/irrlicht/ -I/usr/include/python3.6m/ -I/usr/include/boost"
```  

COMPILER: describes the command used to run your compiler. For example, if I have the g++ compiler installed I might use the command "g++" to run the compiler.

BIN_NAME: defines the name of the binary file that will be compiled and executed. Name it anything you like.

LINKDIRS: a list of directories, separated by spaces, which contain precompiled .so files from any libraries linked by the project. The paths to these directories must be preceded by "-L" and will depend on your OS as well as your installation options. In order to find out what these paths are on your system, look for a folder named after the library (eg. /usr/lib/librt) which contains files with a ".so" extension that are named after the library (eg. /usr/lib/librt/librt.so).

INCDIRS: a list of directories, separated by spaces, which contain header files included by the project. The paths to these directories must be preceded by "-I" and will depend on your OS as well as your installation options. In order to find out what these paths are on your system, look for a folder named after the library (eg. /usr/include/irrlicht) which contains files with a ".h" extension that are named after the library (eg. /usr/include/irrlicht/irrlicht.h).

If any of these variables is incorrect, modify them to so that they are correct. This process can be fairly complex so I suggest reading [this page](http://www.mingw.org/wiki/includepathhowto) if you are unsure of where to start.

Dependencies
------------
All of the following libraries must be installed in order for the program to compile.

* [Irrlicht](http://irrlicht.sourceforge.net/): An open source game engine written in c++ which is used for rendering the state of the simulation.
* python-dev: Contains python header files needed for c to interface with python.
* [Boost](https://www.boost.org/): Provides shared memory allocation for inter-process communication between python and C++ code.
* [librt](https://docs.oracle.com/cd/E19455-01/806-0632/6j9vm89ic/index.html): Provides interfaces for POSIX shared memory objects. 