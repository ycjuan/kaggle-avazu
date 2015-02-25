CXX = g++
CXXFLAGS = -Wall -Wconversion -O3 -fPIC -std=c++0x -march=native -fopenmp
MAIN = mark18
FILES = common.cpp timer.cpp
SRCS = $(FILES:%.cpp=src/%.cpp)
HEADERS = $(FILES:%.cpp=src/%.h)

#DFLAG = -DNOSSE

all: $(MAIN)

mark18: src/train.cpp $(SRCS) $(HEADERS)
	$(CXX) $(CXXFLAGS) $(DFLAG) -o $@ $< $(SRCS)

clean:
	rm -f $(MAIN)
