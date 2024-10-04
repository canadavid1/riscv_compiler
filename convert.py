


with open("a.bin","rb") as f:
    buf = f.read()
    for i in range(0,len(buf),4):
        print(f"0x{int.from_bytes(buf[i:i+4],'little'):08x}")
    
