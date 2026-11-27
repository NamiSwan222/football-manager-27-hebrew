"""Read and write Sports Interactive .fmf archives (Football Manager 26/27).

Layout (worked out from data/game_simulation/languages.fmf):
  header   02 01 'fmf.' 08 00                                    8 bytes, then 00 (1 byte)?
  files    each file is a zstd "seekable format" stream: zstd frames of 4096 uncompressed bytes,
           then a skippable frame (magic 0x184D2A5E) holding the seek table
  index    at the end: a second 'fmf.' header (9 bytes) + one zstd frame:
             u32 len + folder name, u32 count, then per file:
             u32 len + name, u32 len + ext, u64 offset, u64 compressed size, u64 size, u64 time, u64 time
           followed by a u32 0, and the last 8 bytes of the archive... (see index_offset())

    python fmf.py list <archive>
    python fmf.py extract <archive> <name.ext> <out file>
"""
import struct, sys
import zstandard

HEAD = b'\x02\x01fmf.\x08\x00'


def index_offset(d):
    i = d.rfind(HEAD)
    if i <= 0:
        raise ValueError('no fmf index')
    return i


def read_index(d):
    i = index_offset(d)
    z = d.find(b'\x28\xb5\x2f\xfd', i)
    x = zstandard.ZstdDecompressor().decompressobj().decompress(d[z:])
    o = 0

    def s():
        nonlocal o
        n = struct.unpack_from('<I', x, o)[0]
        o += 4 + n
        return x[o - n:o].decode('utf-8')
    folder = s()
    count = struct.unpack_from('<I', x, o)[0]
    o += 4
    files = []
    for _ in range(count):
        name, ext = s(), s()
        off, csize, size, t1, t2 = struct.unpack_from('<QQQQQ', x, o)
        o += 40
        files.append(dict(name=name, ext=ext, offset=off, csize=csize, size=size, t1=t1, t2=t2))
    return folder, files, x[o:], d[i:z]


def data_base(d):
    """Offsets in the index count from the end of the archive header (26 bytes in FM27)."""
    return d.find(bytes.fromhex('28b52ffd'))


def read_file(d, f):
    """Decompress one file: its zstd frames, skipping skippable frames."""
    dc = zstandard.ZstdDecompressor()
    o = data_base(d) + f['offset']
    end, out = o + f['csize'], bytearray()
    while o < end:
        m = struct.unpack_from('<I', d, o)[0]
        if m == 0xFD2FB528:
            ob = dc.decompressobj()
            chunk = d[o:min(end, o + 1 << 20)]
            out += ob.decompress(chunk)
            o += len(chunk) - len(ob.unused_data)
        elif 0x184D2A50 <= m <= 0x184D2A5F:
            o += 8 + struct.unpack_from('<I', d, o + 4)[0]
        else:
            raise ValueError(f'bad frame at {o}')
    return bytes(out)


if __name__ == '__main__':
    d = open(sys.argv[2], 'rb').read()
    folder, files, rest, ihead = read_index(d)
    if sys.argv[1] == 'list':
        print(folder, len(files), 'files; index tail', rest.hex(), 'head', ihead.hex())
        for f in files:
            print(f"{f['name']}{f['ext']:6} off {f['offset']:>10} csize {f['csize']:>9} size {f['size']:>9}")
    elif sys.argv[1] == 'extract':
        f = next(f for f in files if f['name'] + f['ext'] == sys.argv[3])
        data = read_file(d, f)
        assert len(data) == f['size'], (len(data), f['size'])
        open(sys.argv[4], 'wb').write(data)
        print('wrote', len(data))


def seekable(data, level=19):
    """Compress `data` as a zstd seekable stream: 4096-byte frames + seek table (with XXH64 checksums)."""
    import xxhash
    cc = zstandard.ZstdCompressor(level=level)
    out, table = bytearray(), bytearray()
    for i in range(0, len(data), 4096):
        chunk = data[i:i + 4096]
        frame = cc.compress(chunk)
        out += frame
        table += struct.pack('<III', len(frame), len(chunk), xxhash.xxh64(chunk).intdigest() & 0xffffffff)
    n = (len(data) + 4095) // 4096
    table += struct.pack('<IBI', n, 0x80, 0x8F92EAB1)
    out += struct.pack('<II', 0x184D2A5E, len(table)) + table
    return bytes(out)


def rebuild(d, replace, out_path):
    """Copy archive `d` (bytes) to out_path, replacing files {name+ext: new bytes}; the rest is copied verbatim.

    Works for a bare fmf (languages.fmf) and for one inside a wrapper (database `.dat` files start with a
    12-byte `03 01 'dat.' ...` header before the fmf; the header's u32 at fmf+9 = index position - fmf start
    - 9). If the index comes out unchanged (no replacements), its original zstd frame is kept, so a rebuild
    with nothing replaced is byte-identical."""
    folder, files, rest, ihead = read_index(d)
    start = d.find(HEAD)
    base = data_base(d)
    head = bytearray(d[:base])
    body = bytearray()
    new = []
    for f in files:
        key = f['name'] + f['ext']
        if key in replace:
            blob, size = seekable(replace[key]), len(replace[key])
        else:
            blob, size = d[base + f['offset']:base + f['offset'] + f['csize']], f['size']
        new.append(dict(f, offset=len(body), csize=len(blob), size=size))
        body += blob
    idx = bytearray()
    enc = lambda s: struct.pack('<I', len(s.encode('utf-8'))) + s.encode('utf-8')
    idx += enc(folder) + struct.pack('<I', len(new))
    for f in new:
        idx += enc(f['name']) + enc(f['ext']) + struct.pack('<QQQQQ', f['offset'], f['csize'], f['size'], f['t1'], f['t2'])
    idx += rest
    index_pos = base + len(body)
    struct.pack_into('<I', head, start + 9, index_pos - start - 9)
    i = index_offset(d)
    z = d.find(b'\x28\xb5\x2f\xfd', i)
    old = zstandard.ZstdDecompressor().decompressobj().decompress(d[z:])
    frame = d[z:] if bytes(idx) == old else zstandard.ZstdCompressor(level=19).compress(bytes(idx))
    with open(out_path, 'wb') as o:
        o.write(head + body + ihead + frame)
