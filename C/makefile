# Define compiler
# CC = g++

# Compiler flags
CXXFLAGS = -W -g

# OS-independent libraries to be linked
LIBS = -lIrrlicht -lpython3.6m

#Define where to find header files
# INCDIRS = -I/usr/include/irrlicht/

# Define where to find precompiled object files
# LINKDIRS = -L/usr/lib/

# Name of the executable
# BIN_NAME = life

# Object files required to build the executable
PROGRAM_OBJS = Main.o

all: $(BIN_NAME) 

# debug
debugon: CXXFLAGS += -D SHOW_DEBUG -g
debugon: $(BIN_NAME)

# create the executable
$(BIN_NAME): $(PROGRAM_OBJS)
	$(CC) $(LINKDIRS) $(INCDIRS) -o $@ $(PROGRAM_OBJS) $(LIBS) $(PLATFORM_LIBS)

#create an object file (.o) from C file (.c)
%.o : %.cpp
	$(CC) $(CXXFLAGS) $(INCDIRS) -c $< -o $@

clean:
	rm -f *.o core.* *~ $(BIN_NAME) *.bak