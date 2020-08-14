EXEC=chess
SOURCES=$(wildcard *.cpp)
HEADERS=$(SOURCES:.cpp=.hpp)
OBJECTS=$(SOURCES:.cpp=.o)
CCFLAGS=-Wall -Werror -std=c++11
LIBFLAGS=-lsfml-graphics -lsfml-window -lsfml-system
CC=g++

$(EXEC): $(OBJECTS) *.hpp
	$(CC) $(OBJECTS) -o $(EXEC) $(LIBFLAGS)

$(OBJECTS): $(SOURCES) 
	$(CC) -c $(SOURCES) $(CCFLAGS)

clean:
	rm -f $(OBJECTS) $(EXEC)


# $(EXEC): $(OBJECTS)
# 	$(CC) $(OBJECTS) -o $(EXEC)
# %.o: %.cc
# 	$(CC) $(OBJECTS) $(CCFLAGS) -c $< -o $@ $(LIBFLAGS)
# clean:
# 	rm -f $(OBJECTS) $(EXEC)
