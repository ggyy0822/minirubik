ROOT := ../..
OUT := $(ROOT)/output/toolchain
CROSS ?= riscv64-elf-
RIPES ?= $(HOME)/Ripes/build/Ripes.app/Contents/MacOS/Ripes
FLAGS := -O2 -march=rv32i -mabi=ilp32 -msmall-data-limit=0 -mno-relax \
         -ffreestanding -fno-builtin -fno-stack-protector -Wall -Wextra

.PHONY: all check
all: $(OUT)/smoke.elf

$(OUT):
	mkdir -p $(OUT)

$(OUT)/smoke.elf: smoke.c start.S ripes.ld | $(OUT)
	$(CROSS)gcc $(FLAGS) -nostdlib -nostartfiles -Wl,--no-relax \
		-Wl,-T,ripes.ld -Wl,-Map,$(OUT)/smoke.map start.S smoke.c -o $@
	$(CROSS)objdump -d -M no-aliases $@ > $(OUT)/smoke.disasm
	$(CROSS)readelf -h -A $@ > $(OUT)/smoke.attributes.txt
	$(CROSS)size -A $@ > $(OUT)/smoke.sections.txt
	$(CROSS)gcc --version > $(OUT)/compiler.txt
	$(CROSS)gcc -dumpmachine >> $(OUT)/compiler.txt

check: all
	QT_QPA_PLATFORM=offscreen "$(RIPES)" --mode cli --src "$(abspath $(OUT)/smoke.elf)" -t elf \
		--proc RV32_ISS --iret --cycles --exectime --runinfo --timeout 10000 > $(OUT)/iss.txt
	QT_QPA_PLATFORM=offscreen "$(RIPES)" --mode cli --src "$(abspath $(OUT)/smoke.elf)" -t elf \
		--proc RV32_5S --iret --cycles --exectime --runinfo --timeout 10000 > $(OUT)/5s.txt
	grep -q '^12$$' $(OUT)/iss.txt
	grep -q '^12$$' $(OUT)/5s.txt
	grep -q 'Program exited with code: 0' $(OUT)/iss.txt
	grep -q 'Program exited with code: 0' $(OUT)/5s.txt
