# Define compiler
# CC = g++

# Compiler flags
CXXFLAGS = -Wall -W -g

#Link libraries
LIBS = -lIrrlicht

#Define where to find header files
# INCDIRS = -I/usr/include/irrlicht/

# Define where to find precompiled object files
# LINKDIRS = -L/usr/lib/

# Name of the executable
PROGRAM = life

# Object files required to build the executable
PROGRAM_OBJS = Main.o

all: $(PROGRAM) 

# debug
debugon: CXXFLAGS += -D SHOW_DEBUG -g
debugon: $(PROGRAM)

$(PROGRAM): $(PROGRAM_OBJS)
	$(CC) -o $@ $(PROGRAM_OBJS) $(LIBS) $(INCDIRS)

#create an object file (.o) from C file (.c)
%.o : %.cpp
	$(CC) -c $(CXXFLAGS) $< -o $@ $(INCDIRS)

clean:
	rm -f *.o core.* *~ $(PROGRAM) *.bak