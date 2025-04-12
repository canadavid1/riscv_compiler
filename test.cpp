

#include "lib.c"
int main()
{
	unsigned int x = black_box_out(0xc);
	*(char*)(x+24) = 0x8c;
}
