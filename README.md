# Usage
```
    ./compile input_file1.c input_file2.cpp
```
The output (also found in the file `out`) can now be copied into VCB's assembly editor.
Running `./disasm` will disassemble the output to the terminal.

This is definitely not a finished script. There is no guarantee that anything will work and there is a good chance you might find something that does not work properly. 

# Prerequisites
This requires `clang`, `llvm`, `lld` and some version of `python`.

# Modification
The base ISA string, the ABI and the riscv version is found in `compile`.

