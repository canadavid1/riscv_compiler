
void black_box(long in)
{
    asm volatile("": :"r"(in));
}

long black_box_out(long in)
{
    asm volatile("" : "+r"(in));
    return in;
}

void output(long val)
{
    register long v asm("x31") = val;
    asm volatile ("" : : "r"(v));
}
__attribute__((noreturn)) void halt()
{
    while(1) asm volatile("");
}