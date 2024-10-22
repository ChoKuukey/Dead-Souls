SRC = src/server/server.c src/server/data_func.c src/server/db.c
TARGET_WIN = bin/server.exe
TARGET_LINUX = bin/linux_server

.PHONY: все win linux

все: win linux

win: $(TARGET_WIN)

$(TARGET_WIN): src/server/server.o src/server/data_func.o src/server/db.o
	gcc -o $(TARGET_WIN) src/server/server.o src/server/data_func.o src/server/db.o -lws2_32

linux: $(TARGET_LINUX)

$(TARGET_LINUX): src/server/server.o src/server/data_func.o src/server/db.o
	gcc -o $(TARGET_LINUX) ${SRC} -lpq

%.o: %.c
	gcc -c -o $*.o $*.c