

#include "lib.c"
int main()
{
	auto x = black_box_out(0x80000001);
	auto y = black_box_out(0xc0000003);
	if(x == y) while(1) asm volatile(""); 

}
