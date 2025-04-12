#include "lib.c"
signed char a[] = "string";

int main()
{
    for(auto i = a; *i>0; i++) 
    {
        auto register v asm("x31") = *i;
        asm volatile("" : : "r"(v));
    }
}