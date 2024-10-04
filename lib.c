
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
    asm("mv x15, %0" : : "r"(val) : "x15");
}