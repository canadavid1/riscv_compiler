ENTRY(_entry)
SECTIONS
{
. = 0x0004;
.start : { *(.text._entry) }
.text : { *(.text) *(.text.*) }
.data : { *(.data) *(.data.*)  }
.bss : { *(.bss) *(.bss.*) }
}
