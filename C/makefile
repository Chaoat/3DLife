# Define compiler
CC = g++

#Define libraries
# LIBS = -lsfml-graphics -lsfml-window -lsfml-system -lsfml-audio
LIBS = -lIrrlicht

# Compiler flags
CXXFLAGS = -Wall -W -g

# Name of the executable
PROGRAM = life
# Object files required to build the executable
PROGRAM_OBJS = Main.o

all: $(PROGRAM) 

# debug
debugon: CXXFLAGS += -D SHOW_DEBUG -g
debugon: $(PROGRAM)

$(PROGRAM): $(PROGRAM_OBJS)
	$(CC) -I/usr/include/irrlicht/ -L/usr/lib/ -o $@ $(PROGRAM_OBJS) $(LIBS)

#create an object file (.o) from C file (.c)
%.o : %.cpp
	$(CC) -c $(CXXFLAGS) $< -o $@ -I/usr/include/irrlicht/ -L/usr/lib/ 

clean:
	rm -f *.o core.* *~ $(PROGRAM) *.bak

# program: Main.o Game.o Util/FPSCounter.o ResourceManager/ResourceHolder.o States/StatePlaying.o GUI/Button.o GUI/StackMenu.o
# 	g++ Main.o Game.o Util/FPSCounter.o ResourceManager/ResourceHolder.o States/StatePlaying.o GUI/Button.o GUI/StackMenu.o -o myprog -lsfml-graphics -lsfml-window -lsfml-system

# Main.o: Main.cpp
# 	g++ -c Main.cpp

# Main.o: Game.cpp
# 	g++ -c Game.cpp

# Main.o: Util/FPSCounter.cpp
# 	g++ -c Game.cpp

# Main.o: Game.cpp
# 	g++ -c Game.cpp

# Main.o: Game.cpp
# 	g++ -c Game.cpp

# Main.o: Game.cpp
# 	g++ -c Game.cpp

# clean:
# 	rm hello.o hello.exe