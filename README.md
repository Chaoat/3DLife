3DLife
======

Building
-----------
To compile the c++ code you will need both a [c++ compiler](#compiler) and the [project dependencies](#dependancies). Which operating system you use will determine which compilation commands you should use and where you have to point the compiler to find the [project dependencies](#dependancies).  

### Compiler

#### Windows
Install [mingw](http://www.mingw.org/) ro [mingw-64](http://mingw-w64.org/doku.php)

#### Linux
Install [gcc](https://gcc.gnu.org/) 

### Dependancies

All of the following libraries must be installed in order for the program to compile.

#### Irrlicht
Irrlicht is an open source game engine written in c++ which is used for rendering the state of the simulation. 

##### Linux
Irrlicht can be installed using your package manager from linux repositories, eg.

```shell
# pacman -S irrlicht
```

##### Windows
Irrlicht can be downloaded from its [website](http://irrlicht.sourceforge.net/?page_id=10). Windows users must also copy Irrlicht.dll into the [C/](C/) folder.

### Build and Run

Once a compiler and all dependancies are installed, the program can be built and run using the following commands: 

#### Linux
```shell
$ bash C/run.sh
```

#### Windows
```shell
$ C/run
```

Build Problems
--------------

The compiler needs three things in order to successfully compile the project:

1. A compiler
2. Libraries the project depends on
3. Header files from those libraries that are included in the project.

Project libraries are linked in the makefile, and are platform-independant. However the command to run your compiler or the location of your header files may vary. In order to tell the compiler this information, you will have to edit either [C/run.sh](C/run.sh) (linux) or [C/run.bat](C/run.bat) (windows). In the script you will see something similar to:

```shell
make CC=g++ INCDIRS=-I/usr/include/irrlicht/
```  

CC is a variable which describes the command used to run your compiler. INCDIRS describes the directories which contain header files  included in the project. These paths to these files will depend on your OS as well as your installation options, but will always exist in a folder named after the library (eg. /usr/include/irrlicht) and will always have a ".h" extension.

If either of these variables is incorrect, change them to point to the correct compiler command and/or header file locations. This process can be fairly complex so I suggest reading [this page](http://www.mingw.org/wiki/includepathhowto) if you are unsure of where to start.
