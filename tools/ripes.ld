OUTPUT_ARCH(riscv)
ENTRY(_start)
SECTIONS
{
    . = 0x1000;
    .text : { KEEP(*(.text.start)) *(.text .text.*) }
    . = 0x10000000;
    .rodata : { *(.rodata .rodata.*) }
    .data : { *(.data .data.*) *(.sdata .sdata.*) }
    .bss (NOLOAD) : { *(.bss .bss.*) *(.sbss .sbss.*) *(COMMON) }
}
