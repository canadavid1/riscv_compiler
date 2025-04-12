
volatile int global=2;
volatile int global_uninit;
char global_char='a';
const int global_const=4;
const char *const v = "hello";
char second_global_char='b';
char global_array[4]={'c','d','e','f'};
extern int external;

struct {
    int v[8];
} large;

int main()
{
    static int uninit;
    static int init=0x123456;
    return global+global_uninit;
}

void foo() {}