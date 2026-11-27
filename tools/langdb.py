"""FM27 per-language database names: shared\\data\\database\\db\\2700\\2700_fm\\lang_db.dat (read only).

lang_db.dat = 'dat.' wrapper (12 bytes) + an fmf archive (tools/fmf.py) of <language id>_<table>.dat files,
25 language ids x 16 tables. Each table: 03 01 'dat.' u16 version (0x0ea9), u32 record count, records
(u32 db id, then the table's names, each u32 len + UTF-8 + usually a 1-byte grammatical gender, 0xFF = none;
gendered languages add extra forms, e.g. French nationality: masc., fem., masc. plural, fem. plural).

Language ids: 8 English, 1000004 English (US), 2 Arabic, 6 Czech, 7 Dutch, 10 French, 11 German, 12 Greek,
15 Italian, 16 Japanese, 17 Korean, 18 Polish, 19 Portuguese, 1000001 Portuguese (Brazil), 21 Russian,
22 Norwegian, 24 Spanish, 1000000 Spanish (Latin America), 25 Turkish, 30 Swedish, 32 Danish, 58 Thai,
78 Indonesian, 1000002 Chinese (simplified), 1000003 Chinese (traditional). No Hebrew.

Tables (English record counts): 0 awards 3,902 | 2 cities 58,475 | 3 clubs 100,432 | 5 continents 7 |
6 injuries 136 | 7 media 180 | 9 nations 251 | 18 local regions 1,681 | 21 stadiums 52,406 |
23 stage names 288 | 25 competitions 8,084 | 35 derbies 924 | 47 regions 2,532 | 56 agreements 6 |
person_names (empty for English).

    python tools/langdb.py list                       language ids, tables, record counts
    python tools/langdb.py nations <out.json> [id]    nations of one language (default 8): long, short,
                                                      3-letter, nationality (English schema only)
    python tools/langdb.py dump <lang> <table> <out.json>   any table in SCHEMAS (all languages share them)

Record schemas (verified: every table of languages 8, 10, 11, 24 parses to its exact end). S = u32 len + UTF-8,
g = 1-byte grammatical gender (0xFF in English), N = u8 count + count x (S + 3 bytes: the gendered forms,
e.g. French nationality m / f / m pl / f pl; English count 0), bN = N opaque bytes.
  0 awards       id S long g S short g b1
  2 cities       id S name b2
  3 clubs        id S long g S short g S abbr6 S abbr4 S alt4 g S nickname b4 S extra
  9 nations      id S long g S short g S three S nationality N forms
  21 stadiums    id S name S alt_name b3
  25 comps       id S long g S short g S abbr b1
"""
import json, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fmf  # noqa: E402

GAME = r'D:\SteamLibrary\steamapps\common\Football Manager 27'
LANG_DB = os.path.join(GAME, r'shared\data\database\db\2700\2700_fm\lang_db.dat')


def tables(path=LANG_DB):
    d = open(path, 'rb').read()
    _, files, _, _ = fmf.read_index(d)
    return d, files


def table(d, files, name):
    f = next(f for f in files if f['name'] == name)
    return fmf.read_file(d, f)


SCHEMAS = {
    '0': ('SgSgb1', ['long', 'short']),
    '2': ('Sb2', ['name']),
    '3': ('SgSgSSSgSb4S', ['long', 'short', 'abbr6', 'abbr4', 'alt4', 'nickname', 'extra']),
    '9': ('SgSgSSN', ['long', 'short', 'three', 'nationality']),
    '21': ('SSb3', ['name', 'alt_name']),
    '25': ('SgSgSb1', ['long', 'short', 'abbr']),
}
TABLE_NAMES = {'0': 'awards', '2': 'cities', '3': 'clubs', '9': 'nations', '21': 'stadiums', '25': 'comps'}


def parse_table(b, t):
    """Records of table type `t` as [id, parts], parts = list of str (a name field) or bytes (opaque).
    Forms of an N field are str parts followed by their 3 bytes. join_table(header, recs) rebuilds b."""
    import re
    toks = re.findall(r'S|g|N|b\d+', SCHEMAS[t][0])
    n, o, recs = struct.unpack_from('<I', b, 8)[0], 12, []
    for _ in range(n):
        rid = struct.unpack_from('<I', b, o)[0]
        o += 4
        parts = []

        def s():
            nonlocal o
            ln = struct.unpack_from('<I', b, o)[0]
            parts.append(b[o + 4:o + 4 + ln].decode('utf-8', 'surrogateescape'))  # Greek (12) is not all UTF-8
            o += 4 + ln
        for tk in toks:
            if tk == 'S':
                s()
            elif tk == 'g':
                parts.append(b[o:o + 1]); o += 1
            elif tk == 'N':
                k = b[o]
                parts.append(b[o:o + 1]); o += 1
                for _ in range(k):
                    s()
                    parts.append(b[o:o + 3]); o += 3
            else:
                k = int(tk[1:])
                parts.append(b[o:o + k]); o += k
        recs.append([rid, parts])
    assert o == len(b), (t, o, len(b))
    return b[:12], recs


def join_table(header, recs):
    out = bytearray(header)
    struct.pack_into('<I', out, 8, len(recs))
    for rid, parts in recs:
        out += struct.pack('<I', rid)
        for p in parts:
            if isinstance(p, str):
                e = p.encode('utf-8', 'surrogateescape')
                out += struct.pack('<I', len(e)) + e
            else:
                out += p
    return bytes(out)


def fields(parts, t):
    """The named string fields of a record (first len(names) str parts) -> dict; forms -> 'forms' list."""
    strs = [p for p in parts if isinstance(p, str)]
    names = SCHEMAS[t][1]
    d = dict(zip(names, strs))
    if len(strs) > len(names):
        d['forms'] = strs[len(names):]
    return d


def nations_en(b):
    """English nation table: id, long+gender, short+gender, 3-letter, nationality+gender."""
    n, o, out = struct.unpack_from('<I', b, 8)[0], 12, []

    def s():
        nonlocal o
        ln = struct.unpack_from('<I', b, o)[0]
        o += 4 + ln
        return b[o - ln:o].decode('utf-8')
    for _ in range(n):
        i = struct.unpack_from('<I', b, o)[0]
        o += 4
        long_ = s(); o += 1
        short = s(); o += 1
        three = s()
        nat = s(); o += 1
        out.append(dict(id=i, long=long_, short=short, three=three, nationality=nat))
    assert o == len(b), 'not the English nation schema'
    return out


if __name__ == '__main__':
    d, files = tables()
    if sys.argv[1] == 'list':
        langs = {}
        for f in files:
            if f['name'].endswith('person_names'):
                lang, t = f['name'][:-len('person_names')], 'person_names'
            else:
                lang, _, t = f['name'].partition('_')
            b = table(d, files, f['name']) if f['size'] >= 12 else b''
            langs.setdefault(lang, {})[t] = struct.unpack_from('<I', b, 8)[0] if len(b) >= 12 else 0
        for lang, ts in langs.items():
            print(lang, ts)
    elif sys.argv[1] == 'dump':
        _, recs = parse_table(table(d, files, f'{sys.argv[2]}_{sys.argv[3]}'), sys.argv[3])
        rows = [dict(id=i, **fields(p, sys.argv[3])) for i, p in recs]
        json.dump(rows, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print(len(rows), 'records ->', sys.argv[4])
    elif sys.argv[1] == 'nations':
        lang = sys.argv[3] if len(sys.argv) > 3 else '8'
        rows = nations_en(table(d, files, f'{lang}_9'))
        json.dump(rows, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print(len(rows), 'nations ->', sys.argv[2])
