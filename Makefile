SRC = src/server/server.c src/server/data_func.c src/server/db.c
TARGET_WIN = bin/server.exe
TARGET_LINUX = bin/linux_server
LIBPQ_LINK = C:/"Program Files"/PostgreSQL/16/lib
# LIBPQ_LINK = D:/PostgreSQL/16/lib

.PHONY: all win linux

all: win linux

win: $(TARGET_WIN)

$(TARGET_WIN): src/server/server.o src/server/data_func.o src/server/db.o
	gcc -o $(TARGET_WIN) ${SRC} -lws2_32 -L${LIBPQ_LINK} -lpq 

linux: $(TARGET_LINUX)

$(TARGET_LINUX): src/server/server.o src/server/data_func.o src/server/db.o
	gcc -o $(TARGET_LINUX) ${SRC} -lpq

%.o: %.c
	gcc -c -o $*.o $*.c