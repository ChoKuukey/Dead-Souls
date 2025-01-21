GENERATE_CONFIRM_CODE_SRC = ../../test/data_test/generate_confirm_code.c ../../src/server/data_func.c

GENERATE_CONFIRM_CODE_TARGET_WIN = ../../test/data_test/generate_confirm_code.exe
GENERATE_CONFIRM_CODE_TARGET_LINUX = ../../test/data_test/generate_confirm_code


genconcode_win: $(GENERATE_CONFIRM_CODE_TARGET_WIN)

$(GENERATE_CONFIRM_CODE_TARGET_WIN): ${GENERATE_CONFIRM_CODE_SRC}
	gcc -o $(GENERATE_CONFIRM_CODE_TARGET_WIN) ${GENERATE_CONFIRM_CODE_SRC}

genconcode_linux: $(GENERATE_CONFIRM_CODE_TARGET_LINUX)

$(GENERATE_CONFIRM_CODE_TARGET_LINUX): ${GENERATE_CONFIRM_CODE_SRC}
	gcc -o $(GENERATE_CONFIRM_CODE_TARGET_LINUX) ${GENERATE_CONFIRM_CODE_SRC}

%.o: %.c
	gcc -c -o $*.o $*.c
