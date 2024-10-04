# Usage
```
    ./compile input_file1.c input_file2.cpp
```
The output (also found in the file `out`) can now be copied into VCB's assembly editor.
Running `./disasm` will disassemble the output to the terminal.


# Prerequisites
This requires `clang`, `llvm`, `lld` and some version of `python`.

# Modification
The base ISA string, the ABI and the riscv version is found in `compile`.

