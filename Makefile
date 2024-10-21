SRC = src/server/server.c src/server/common.h
TARGET_WIN = bin/server.exe
TARGET_LINUX = bin/linux_server

.PHONY: all win-linux

all: win-linux

win: $(TARGET_WIN)

$(TARGET_WIN): src/server/server.o
	gcc -o $(TARGET_WIN) src/server/server.o -lws2_32

src/server/server.o: $(SRC)
	gcc -c -o src/server/server.o src/server/server.c

linux: $(TARGET_LINUX)

$(TARGET_LINUX): src/server/server.o
	gcc -o $(TARGET_LINUX) src/server/server.o

src/server/server.o: $(SRC)
	gcc -c -o src/server/server.o src/server/server.c
