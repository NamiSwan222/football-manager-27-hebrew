"""List a PE file's imports: py -I peimports.py <exe> [dllname-filter]"""
import sys, struct
d = open(sys.argv[1], 'rb').read()
flt = sys.argv[2].lower() if len(sys.argv) > 2 else None
pe = struct.unpack_from('<I', d, 0x3c)[0]
nsec = struct.unpack_from('<H', d, pe + 6)[0]; opt = pe + 24; osz = struct.unpack_from('<H', d, pe + 20)[0]
secs = [struct.unpack_from('<8sIIII', d, opt + osz + i * 40) for i in range(nsec)]
def r2o(rva):
    for n, vs, va, rs, ro in secs:
        if va <= rva < va + max(vs, rs): return rva - va + ro
def cstr(o): return d[o:d.index(b'\0', o)].decode()
o = r2o(struct.unpack_from('<I', d, opt + 112 + 8)[0])
while True:
    ilt, ts, fc, name, iat = struct.unpack_from('<IIIII', d, o); o += 20
    if name == 0: break
    dll = cstr(r2o(name))
    if flt and flt not in dll.lower(): continue
    p = r2o(ilt or iat); fns = []
    while True:
        v = struct.unpack_from('<Q', d, p)[0]; p += 8
        if v == 0: break
        fns.append(f'#{v & 0xffff}' if v >> 63 else cstr(r2o(v & 0x7fffffff) + 2))
    print(dll, fns if flt else len(fns))
