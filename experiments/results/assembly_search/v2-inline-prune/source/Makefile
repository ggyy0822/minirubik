# AI-generated build harness; search fragments retain their own provenance.
ROOT := ../..
OUT := $(ROOT)/output/assembly_search
CROSS ?= riscv64-elf-
INPUT ?= 21345671111111
BASE := ../rv32_baseline
TABLES := $(ROOT)/output/rv32_baseline/tables.c
FLAGS := -O2 -std=c99 -march=rv32i -mabi=ilp32 -msmall-data-limit=0 -mno-relax -ffreestanding -fno-builtin -fno-stack-protector -Wall -Wextra
SOURCES := student_search.S quarter_step.S heuristic.S init_frame.S $(BASE)/state.c $(BASE)/main.c $(BASE)/start.S
ELF := $(OUT)/$(INPUT).elf
.PHONY: all
all: $(ELF)
$(OUT):
	mkdir -p $@
$(TABLES):
	$(MAKE) -C $(BASE) ../../output/rv32_baseline/tables.c
$(ELF): $(SOURCES) $(wildcard *.inc) $(BASE)/target.h ../toolchain/ripes.ld $(TABLES) | $(OUT)
	$(CROSS)gcc $(FLAGS) -DCUBE_INPUT='"$(INPUT)"' -nostdlib -nostartfiles -Wl,--no-relax -Wl,-T,../toolchain/ripes.ld -Wl,-Map,$(OUT)/$(INPUT).map $(SOURCES) $(TABLES) -o $@
	$(CROSS)objdump -d -M no-aliases $@ > $(OUT)/$(INPUT).disasm
	$(CROSS)size -A $@ > $(OUT)/$(INPUT).sections.txt
	$(CROSS)readelf -h -A $@ > $(OUT)/$(INPUT).attributes.txt
