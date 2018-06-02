3DLife
======

Building
-----------
To compile the c++ code you will need both a c++ compiler and the [project dependencies](#dependencies). Which operating system you use will determine which compilation commands you should use and where you have to point the compiler to find the [project dependencies](#dependencies).  

### Windows
1. Install a c++ compiler, eg. [mingw](http://www.mingw.org/) or [mingw-64](http://mingw-w64.org/doku.php).
2. Install [Irrlicht](http://irrlicht.sourceforge.net/). Copy Irrlicht.dll into the [./C](./C) folder.
3. Ensure you have the python-dev headers. Header files are included with the python binary on windows, eg. c:\Python36\include.
4. Build and run the program with the command:
```shell
$ C/run
```

### Linux
1. Install a c++ compiler, eg. [gcc](https://gcc.gnu.org/).
2. Install [Irrlicht](http://irrlicht.sourceforge.net/).
3. Ensure you have the python-dev headers. Some distributions include headers in the installation eg. usr/include/python3.6m, otherwise install the python-dev package for your distribution.
4. Build and run the program with the command:
```shell
$ bash C/run.sh
```

### Dependencies
All of the following libraries must be installed in order for the program to compile.

* [Irrlicht](http://irrlicht.sourceforge.net/): An open source game engine written in c++ which is used for rendering the state of the simulation.
* python-dev: Contains python header files needed for c to interface with python.

Build Problems
--------------

The compiler needs three things in order to successfully compile the project:

1. A compiler
2. Libraries the project depends on
3. Header files from those libraries that are included in the project.

Project libraries are linked in the makefile, and are platform-independant. However the command to run your compiler or the location of your header files may vary. In order to tell the compiler this information, you will have to edit either [run.sh](./run.sh) (linux) or [run.bat](./run.bat) (windows). In the script you will see something similar to:

```shell
make CC=g++ INCDIRS="-I/usr/include/irrlicht/ -I/usr/include/python3.6m/"
```  

CC is a variable which describes the command used to run your compiler. INCDIRS describes the directories which contain header files included by the project. The paths to these files are preceded by "-I" and will depend on your OS as well as your installation options, however header files will always be in a folder named after the library (eg. /usr/include/irrlicht) and will always have a ".h" extension (eg. /usr/include/irrlicht/irrlicht.h).

If either of these variables is incorrect, change them to point to the correct compiler command and/or header file locations. This process can be fairly complex so I suggest reading [this page](http://www.mingw.org/wiki/includepathhowto) if you are unsure of where to start.
