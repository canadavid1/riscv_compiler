
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
import os
import re
from collections import defaultdict    

def get_disasm_line(line: str) -> str | None:
    a = re.match(r'([ 0-9a-f]{8}):((?: [0-9a-f]{2})+) *\t(.+)',line)
    # if a:print(a[1],a[2],a[3],sep=" | ")
    return (int(a[1],16),('c.' if len(a[2])==6 else '')+a[3],len(a[2])//3) if a else (None,None,None)

def disassemble_section(section: str,file: str) -> list[str]:
    return os.popen(f"llvm-objdump -d -j {section} {file}").readlines()[4:]


FILE = "a.out"

def sections(f: ELFFile):
    n = f.num_sections()
    for i in range(1,n):
        yield f.get_section(i)

f = open(FILE,'rb')
if True:
    binout = bytearray() # binary data to output
    disasm: dict[int,str] = {} # map from location to disassembly
    symb: defaultdict[int,list[str]] = defaultdict(list) # map from location to list of symbols
    file = ELFFile(f)
    for sec in sections(file):
        addr = sec.header.sh_addr
        data = sec.data()
        if addr:
            # symb[addr].append("S" + sec.name)
            if len(binout) < addr+len(data):
                binout.extend([0]*(addr+len(data)-len(binout)))
            for i,v in enumerate(sec.data()):
                binout[addr+i] = v
    for l in disassemble_section(".start",FILE) + disassemble_section(".text",FILE):
        pos,dis,l = get_disasm_line(l)
        if pos is not None:
            disasm[pos] = dis
    symtab = file.get_section_by_name(".symtab")
    if not symtab or not isinstance(symtab,SymbolTableSection):
        print("symbol table not found")
        exit(1)
    for i in range(1,symtab.num_symbols()):
        sym = symtab.get_symbol(i)
        if sym.name and sym.name[0] != '$' and sym.entry.st_size > 0:
            symb[sym.entry['st_value']].append(sym.name)

def emit(binout: bytearray,disasm: dict[int,str],symb: dict[int,list[str]]):
    for i in range(4,len(binout),4):
        ass = []
        out = False
        v = int.from_bytes(binout[i:i+4],'little')
        for j in range(i,i+4):
            for k in symb[j]:
                yield f"#{j:4x}   {k}:"
            if j in disasm:
                if not out:
                    yield f"0x{v:08x} #{j:3x} {disasm[j]}"
                    out = True
                else:
                    yield f"           #{j:3x} {disasm[j]}"
        if not out:
            yield f"0x{v:08x}"

print(*emit(binout,disasm,symb),sep="\n")