ROOT := ../..
OUT := $(ROOT)/output/rv32_baseline
HOST_CC ?= cc
CROSS ?= riscv64-elf-
INPUT ?= 21345671111111
FLAGS := -O2 -std=c99 -march=rv32i -mabi=ilp32 -msmall-data-limit=0 -mno-relax \
         -ffreestanding -fno-builtin -fno-stack-protector -Wall -Wextra
SOURCES := search.c state.c main.c start.S
ELF := $(OUT)/$(INPUT).elf

.PHONY: all native-check
all: $(ELF)

$(OUT):
	mkdir -p $(OUT)

$(OUT)/generate: generate.c ../ida_reference.c $(ROOT)/solver.c | $(OUT)
	$(HOST_CC) -O2 -std=c99 -Wall -Wextra -Wno-unused-function $< -o $@

$(OUT)/tables.c: $(OUT)/generate
	$< > $@.tmp
	mv $@.tmp $@

$(ELF): $(SOURCES) target.h ../toolchain/ripes.ld $(OUT)/tables.c
	$(CROSS)gcc $(FLAGS) -DCUBE_INPUT='"$(INPUT)"' -nostdlib -nostartfiles \
		-Wl,--no-relax -Wl,-T,../toolchain/ripes.ld -Wl,-Map,$(OUT)/$(INPUT).map \
		$(SOURCES) $(OUT)/tables.c -o $@
	$(CROSS)objdump -d -M no-aliases $@ > $(OUT)/$(INPUT).disasm
	$(CROSS)size -A $@ > $(OUT)/$(INPUT).sections.txt
	$(CROSS)readelf -h -A $@ > $(OUT)/$(INPUT).attributes.txt

$(OUT)/verify_native: verify_native.c search.c state.c target.h ../ida_reference.c $(ROOT)/solver.c $(OUT)/tables.c
	$(HOST_CC) -O2 -std=c99 -Wall -Wextra -Wno-unused-function verify_native.c \
		search.c state.c $(OUT)/tables.c -o $@

native-check: $(OUT)/verify_native
	$(OUT)/verify_native --check
