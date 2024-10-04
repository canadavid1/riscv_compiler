

extern int main();
__attribute((noreturn)) void _entry() {
    asm("li sp,0x400000");
    register int ret_val asm("a0");
    asm volatile("jal main" :"=r"(ret_val));
    while(1);
}