
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

// unsigned long popcount(unsigned long in)
// {
//     unsigned long c;
//     asm ("cpop %0, %1" : "=r"(c) : "r"(in));
//     return c;
// }

void halt()
{
    asm volatile("ebreak");
}