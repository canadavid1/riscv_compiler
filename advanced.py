
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
import elftools.elf as elf
import os
import re
from collections import defaultdict    

def convert_line(line: str) -> str | None:
    """ converts lines:
    00000004 <_entry>:                              -> origin 0x00001 ; _entry:
        4: 37 01 40 00   lui     sp, 0x400          -> 0x00400137   ; lui     sp, 0x400 
        8: ef 00 80 00   jal     0x10 <main>        -> 0x008000ef   ; jal     0x10 <main>
    """
    if line == '' or line == '\n': return None
    if (a:=re.match('([0-9a-fA-F]{8}) <(.*)>:',line.strip())):
        addr = int(a[1],16)
        sym = a[2]
        return f"origin 0x{addr//4:05x} # {sym}:\t"
    addr,i0,i1,i2,i3,instr = line.strip().split(None,5)
    return f"0x{i3}{i2}{i1}{i0}\t# {addr} \t{instr}"

def get_disasm_line(line: str) -> str | None:
    a = re.match(r'([ 0-9a-f]{8}):((?: [0-9a-f]{2})+) *\t(.+)',line)
    # if a:print(a[1],a[2],a[3],sep=" | ")
    return (int(a[1],16),('c.' if len(a[2])==6 else '')+a[3],len(a[2])//3) if a else (None,None,None)



def disassemble_symbol(symbol: str,file: str) -> list[str]:
    return os.popen(f"llvm-objdump --disassemble-symbols={symbol} {file}").readlines()[6:]

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
            symb[addr].append("S" + sec.name)
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
            # print(f"{sym.name:20}",sym.entry)
            symb[sym.entry['st_value']].append(sym.name)
    # for i,v in enumerate(binout):
    #     if i in symb:
    #         # print("\n",f"{i:3x}",*symb[i],sep=" ",end=":\n\t")
    #     print(f"{v:02x}",end=" ")
    #     if i in edisasm:
    #         # print("\t",disasm[i],end="\n\t")
    # print()

def emit(binout: bytearray,disasm: dict[int,str],symb: dict[int,list[str]]):
    for i in range(4,len(binout),4):
        ass = []
        for j in range(i,i+4):
            for k in symb[j]:
                yield f"#{j:4x}   {k}:" if j == i else f"#{i:4x}{j-i:+1} {k}:"
            if j in disasm:
                ass.append(disasm[j])
        v = int.from_bytes(binout[i:i+4],'little')
        if not ass:
            yield f"0x{v:08x}"
            continue
        yield f"0x{v:08x} #{i:3x} {ass[0]}"
        for a in ass[1:]:
            yield f"           #    {a}"

print(*emit(binout,disasm,symb),sep="\n")