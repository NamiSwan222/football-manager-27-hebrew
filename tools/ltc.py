"""Read and write Football Manager compiled language files (.ltc, magic "ctl.").

Layout (FM27 english.ltc):
  03 01 'ctl.' u16 16 | u32 index_pos-8 | u32 0 | u32 len + language name | u32 1001
  string table: per string  01 | u32 len | UTF-8 bytes          (198,791 strings)
  index at index_pos: u32 count, then count x (u32 id, u32 offset-8 of the string record)
Several index entries can share an id: the game picks one of those variants at random.
"""
import struct


def read(path):
    d = open(path, 'rb').read()
    assert d[2:6] == b'ctl.', 'not an ltc file'
    index_pos = struct.unpack_from('<I', d, 8)[0] + 8
    n = struct.unpack_from('<I', d, 16)[0]
    name = d[20:20 + n].decode('utf-8')
    head = d[:20 + n + 4]
    o, strings, at = len(head), [], {}
    variants = {}
    while o < index_pos:
        k = d[o]  # number of variants in this record (1, or 2+ for gendered languages: male, female...)
        at[o - 8] = len(strings)
        p, vs = o + 1, []
        for _ in range(k):
            ln = struct.unpack_from('<I', d, p)[0]
            vs.append(d[p + 4:p + 4 + ln].decode('utf-8'))
            p += 4 + ln
        if k > 1:
            variants[len(strings)] = vs
        strings.append(vs[0])
        o = p
    count = struct.unpack_from('<I', d, index_pos)[0]
    index = [struct.unpack_from('<II', d, index_pos + 4 + 8 * i) for i in range(count)]
    tail = d[index_pos + 4 + 8 * count:]
    # (id, string number, flag): the top bit of the offset is a flag we keep as is
    entries = [(sid, at[off & 0x7fffffff], off & 0x80000000) for sid, off in index]
    return dict(head=head, name=name, strings=strings, index=entries, tail=tail, variants=variants)


def write(path, ltc, strings):
    """Write `ltc` with its strings replaced by `strings` (same count and order)."""
    assert len(strings) == len(ltc['strings'])
    body, offs = bytearray(ltc['head']), []
    for s in strings:
        b = s.encode('utf-8')
        offs.append(len(body) - 8)
        body += b'\x01' + struct.pack('<I', len(b)) + b
    index_pos = len(body)
    struct.pack_into('<I', body, 8, index_pos - 8)
    body += struct.pack('<I', len(ltc['index']))
    for sid, num, flag in ltc['index']:
        body += struct.pack('<II', sid, offs[num] | flag)
    body += ltc['tail']
    with open(path, 'wb') as f:
        f.write(body)
