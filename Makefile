SRC = src/server/server.c src/server/common.h
TARGET = bin/server.exe

.PHONY: all

all: $(TARGET)

$(TARGET): src/server/server.o
	gcc -o $(TARGET) src/server/server.o

src/server/server.o: $(SRC)
	gcc -c -o src/server/server.o src/server/server.c

