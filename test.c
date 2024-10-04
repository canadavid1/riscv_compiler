

#include "lib.c"

int main()
{
	int x=1,y=1;
	while(1)
	{
		x += y;
		y += x;
		black_box(y); // stop optimizations
	}
}
