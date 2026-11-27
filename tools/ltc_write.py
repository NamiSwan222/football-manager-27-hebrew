"""Full-fidelity reader/writer for FM compiled language files (.ltc), and our own ltf -> ltc compiler.

Layout (all little-endian), checked on every shipped FM27 .ltc and on FM's own compile of a user .ltf:
  03 01 'ctl.' u16 16              magic
  u32 index_pos - 8
  u32 source size                  0 in shipped files; size in bytes of the .ltf FM compiled it from
  u32 len + language name          ("Français"; for a user language: LANGNAME)
  u32 1001 | 0                     1001 in shipped files, 0 in FM's compile of a user .ltf
  records                          per record: u8 n, then n x (u32 len + UTF-8). n = 1, or several gender
                                   variants: shipped gendered languages store [M, F], [MM, MF, FM, FF]... (no
                                   base); FM's ltf compiler stores [base, <ltf variants in file order>].
  index (at index_pos)             u32 count, count x (u32 id, u32 record offset - 8 | 0x80000000 flag)
                                   id = 0x10000000 + ltf key number (shipped files also have ~600 ids in
                                   0x2..0x6 namespaces and ~1000 flagged entries; FM's ltf compile has neither)
  tail                             u16 count + GENDERINFO article/contraction tables (French, German...);
                                   u32 0 when there are none (English, Arabic, every user ltf)

    python tools/ltc_write.py roundtrip <file.ltc>...           parse + write, compare bytes
    python tools/ltc_write.py compile <file.ltf> <out.ltc>      our compile, FM's record shape [base, variants]
    python tools/ltc_write.py hebrew <out.ltc> [--ltf <file>] [--markers] [--no-rli]
        Hebrew from translation/he/units.json (English from work/en, tools/extract.py): split units -> [m, f]
        records (no base, like French), everything else one record with the base text. --ltf: the .ltf that will sit next to it (its size
        goes into the header so FM sees the .ltc as compiled from it). --markers: prefix "L^" / "LM~" /
        "LF~" (in-game test: shows the text came from this file and which variant was picked); untranslated
        families are then written in French form too, from their English variants ("LM~", "LMF~"...).
"""
import json, os, re, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ltf  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.expandvars(r'%USERPROFILE%\Documents\Sports Interactive\Football Manager 27\languages\example.ltf')
MAGIC = b'\x03\x01ctl.\x10\x00'
ID_BASE = 0x10000000
FLAG = 0x80000000
RLI, PDI = '⁧', '⁩'
HEBREW = re.compile('[֐-׿]')
PRONOUN = re.compile(r'\[%person#(\w+)-(?:he|she|his|her|him|himself|herself|He|She|His|Her|Him)\]')


def parse(path):
    d = open(path, 'rb').read()
    assert d[:8] == MAGIC, 'not an ltc file'
    index_pos = struct.unpack_from('<I', d, 8)[0] + 8
    source_size = struct.unpack_from('<I', d, 12)[0]
    n = struct.unpack_from('<I', d, 16)[0]
    name = d[20:20 + n].decode('utf-8')
    o = 20 + n
    trailer = struct.unpack_from('<I', d, o)[0]
    o += 4
    records, at = [], {}
    while o < index_pos:
        at[o - 8] = len(records)
        k, o = d[o], o + 1
        vs = []
        for _ in range(k):
            ln = struct.unpack_from('<I', d, o)[0]
            vs.append(d[o + 4:o + 4 + ln].decode('utf-8', 'surrogateescape'))
            o += 4 + ln
        records.append(vs)
    assert o == index_pos
    count = struct.unpack_from('<I', d, o)[0]
    index = []
    for i in range(count):
        sid, off = struct.unpack_from('<II', d, o + 4 + 8 * i)
        index.append((sid, at[off & ~FLAG], bool(off & FLAG)))
    tail = d[o + 4 + 8 * count:]
    return dict(name=name, source_size=source_size, trailer=trailer, records=records, index=index, tail=tail)


def build(ltc):
    name = ltc['name'].encode('utf-8')
    body = bytearray(MAGIC + b'\0' * 8 + struct.pack('<I', len(name)) + name + struct.pack('<I', ltc['trailer']))
    offs = []
    for vs in ltc['records']:
        assert 1 <= len(vs) <= 255
        offs.append(len(body) - 8)
        body.append(len(vs))
        for v in vs:
            b = v.encode('utf-8', 'surrogateescape')
            body += struct.pack('<I', len(b)) + b
    struct.pack_into('<II', body, 8, len(body) - 8, ltc['source_size'])
    body += struct.pack('<I', len(ltc['index']))
    for sid, rec, flag in ltc['index']:
        body += struct.pack('<II', sid, offs[rec] | (FLAG if flag else 0))
    return bytes(body + ltc['tail'])


def write(path, ltc):
    with open(path, 'wb') as f:
        f.write(build(ltc))


# ---- ltf ------------------------------------------------------------------------------------------

def read_ltf(path):
    """[(key, english, STR-1)] in file order (like ltf.read, but keeps the translations)."""
    out, cur, mode = [], None, None
    for line in open(path, encoding='utf-8-sig').read().split('\n'):
        m = ltf.KEY.match(line)
        if m:
            cur = [m.group(1), m.group(2), None]
            out.append(cur)
            mode = 'key'
            continue
        m = ltf.STR.match(line)
        if m and cur is not None:
            cur[2] = m.group(2)
            mode = 'str'
            continue
        if cur is None:
            continue
        if mode == 'key':
            cur[1] += '\n' + line
        # STR continuation lines: FM keeps only the first line of an STR, so they are dropped here too
    return [(k, en.rstrip('\n'), (s or '').rstrip('\n')) for k, en, s in out]


def ltf_header(path):
    head = {}
    for line in open(path, encoding='utf-8-sig'):
        if line.startswith('KEY-'):
            break
        if ':' in line and not line.startswith('#'):
            k, v = line.split(':', 1)
            head[k.strip()] = v.strip()
    return head


def families(entries):
    """{base key number: [entries of the family in file order, base first]}"""
    fam = {}
    for e in entries:
        fam.setdefault(int(e[0].split('-')[0]), []).append(e)
    for k, es in fam.items():
        es.sort(key=lambda e: '-' in e[0])  # base first, variants keep file order
    return fam


def assemble(name, source_size, records_by_id):
    ids = sorted(records_by_id)
    return dict(name=name, source_size=source_size, trailer=0, records=[records_by_id[i] for i in ids],
                index=[(i, n, False) for n, i in enumerate(ids)], tail=struct.pack('<I', 0))


COMMENT = re.compile(r'\[(?!%)[^\]]*\]')
ESC = re.compile(r'\\(.)')


def fm_text(s):
    """FM's compile of one STR: [...] notes that are not tokens removed, backslash escapes resolved."""
    s = COMMENT.sub("", s).strip()
    return ESC.sub(lambda m: '\n' if m.group(1) == 'n' else m.group(1), s)


def compile_ltf(path):
    """What FM's compiler makes of a user ltf (record [base, variants...], sorted by id)."""
    entries = read_ltf(path)
    recs = {}
    for k, es in families(entries).items():
        if not fm_text(es[0][1]):  # FM drops a key whose English is empty after comment removal (648473)
            continue
        recs[ID_BASE + k] = [fm_text(s if s else ltf.plain(en)) for _, en, s in es]
    return assemble(ltf_header(path).get('LANGNAME', ''), os.path.getsize(path), recs)


# ---- Hebrew ---------------------------------------------------------------------------------------

def hebrew(ltf_for_size=None, markers=False, rli=True):
    entries = ltf.read(TEMPLATE)[1]
    import extract  # English from work/en (tools/extract.py), Hebrew from translation/he/units.json
    units = extract.load_units()
    by_en = {units[u]['en']: he for u, he in extract.load_he()[0].items()}
    wrap = (lambda s: RLI + s + PDI if HEBREW.search(s) else s) if rli else (lambda s: s)
    recs, stats = {}, {'split': 0, 'plain': 0, 'english': 0}
    fam = {}
    for k, en in entries:
        fam.setdefault(int(k.split('-')[0]), []).append((k, en))
    for k, es in fam.items():
        base = next((en for key, en in es if '-' not in key), None)
        if base is None:  # (no such family in FM27, kept for safety)
            base = es[0][1]
        if not fm_text(base):  # FM drops these too
            continue
        en = ltf.plain(base)
        he = by_en.get(en)
        if isinstance(he, dict):
            # Each variant must carry its gender as a token, as in French: the engine matches the variant's
            # [%male#N]/[%female#N] tokens against the people passed in. Add a -hidden one if missing.
            p = (PRONOUN.search(en) or re.search(r'\[%person#(\w+)', en))
            p = p.group(1) if p else '1'
            m, f = he['m'], he['f']
            if not re.search(r'\[%male#', m):
                m += f'[%male#{p}-hidden]'
            if not re.search(r'\[%female#', f):
                f += f'[%female#{p}-hidden]'
            m, f = wrap(fm_text(m)), wrap(fm_text(f))
            recs[ID_BASE + k] = ['LM~' + m, 'LF~' + f] if markers else [m, f]
            stats['split'] += 1
        elif he:
            he = wrap(fm_text(he))
            recs[ID_BASE + k] = ['L^' + he] if markers else [he]
            stats['plain'] += 1
        elif markers and len(es) > 1:
            # test only: an untranslated family in French form, its English variants without the base
            recs[ID_BASE + k] = ['L' + key.split('-')[1] + '~' + fm_text(v) for key, v in es if '-' in key]
            stats['english variants'] = stats.get('english variants', 0) + 1
        else:
            en = fm_text(base)
            recs[ID_BASE + k] = ['L^' + en] if markers else [en]
            stats['english'] += 1
    size = os.path.getsize(ltf_for_size) if ltf_for_size else 0
    return assemble('Hebrew', size, recs), stats


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'roundtrip':
        for p in a[1:]:
            ok = build(parse(p)) == open(p, 'rb').read()
            print(p, 'byte-identical' if ok else 'DIFFERENT')
    elif a[0] == 'compile':
        out = compile_ltf(a[1])
        write(a[2], out)
        print(len(out['records']), 'records ->', a[2])
    elif a[0] == 'hebrew':
        opt = lambda f: a[a.index(f) + 1] if f in a else None
        out, st = hebrew(opt('--ltf'), '--markers' in a, '--no-rli' not in a)
        write(a[1], out)
        print(len(out['records']), 'records ->', a[1], st, 'source size', out['source_size'])
