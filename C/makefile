# Define compiler
# CC = g++

# Compiler flags
CXXFLAGS = -W -g

#Link libraries
LIBS = -lIrrlicht -lpython3.6m

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

# create the executable
$(PROGRAM): $(PROGRAM_OBJS)
	$(CC) $(INCDIRS) -o $@ $(PROGRAM_OBJS) $(LIBS)

#create an object file (.o) from C file (.c)
%.o : %.cpp
	$(CC) $(INCDIRS) -c $(CXXFLAGS) $< -o $@

clean:
	rm -f *.o core.* *~ $(PROGRAM) *.bak