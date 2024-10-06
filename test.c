

#include "lib.c"
extern void foo();
int global=123;
int main()
{
	int x=1,y=1;
	foo();
	while(1)
	{
		x += y;
		y += x;
		black_box(y); // stop optimizations
	}
}
