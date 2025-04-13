#include "lib.c"


struct A {
    A() {
        MARK(4);
    }

};

A arr[100];

int main()
{
    black_box((long)arr);
}