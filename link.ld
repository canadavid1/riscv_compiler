ENTRY(_entry)
SECTIONS
{
. = 0x0004;
.start : { *(.text._entry) *(.start) }
.text : { *(.text) *(.text.*) }
.sdata : ALIGN(4) {
    PROVIDE(global_pointer$ = . + 0x800);
    *(.sdata) *(.sdata.*) *(.sbss) *(.sbss.*) 
}
.rodata : ALIGN(4) { *(.rodata) *(.rodata.*) }
.data : ALIGN(4) { *(.data) *(.data.*)  }
.bss : ALIGN(4) { *(.bss) *(.bss.*) }
}
