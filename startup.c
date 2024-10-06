

extern int main();
__attribute((naked,section(".start"))) void _entry() {
    asm(
        ".option push;"
        ".option norelax;"
        "la gp, global_pointer$;"
        ".option pop;"
        "li sp,0x400000;"
        "call main;"
        "j .;"
    );
}
