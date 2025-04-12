#include "lib.c"


int arr[] = {1, 2, 3, 4, 5};

int main()
{
    int v = 0;
    for(auto i : arr) v += i;
    black_box(v);
}