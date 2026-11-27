"""Write the Hebrew copy of FM27's lang_db.dat: the English (8_*) name tables carry Hebrew for every record in
translation/he/dbnames/<category>.json; everything else (other languages, out-of-scope records, all non-name
bytes, and the English of every field we have no Hebrew for) is copied unchanged from the game's own
lang_db.dat, which is only read. The proxy maps the game's open of lang_db.dat to this copy in Hebrew sessions
(pack/redirect.cfg), so a normal launch never sees it.

translation/he/dbnames/<category>.json = {"<db id>": {field: Hebrew}} (no English; python tools/merge.py
--dbnames folds the translators' work/dbnames/done batches into it):
  nations        long, short                       -> 8_9  long, short
  nationalities  m, f, mpl, fpl                    -> 8_9  nationality = m (English tables have one form)
  competitions*  long, short [, abbr]              -> 8_25
  clubs          long, short [, abbr6, nickname]   -> 8_3
  stadiums       name [, alt_name]                 -> 8_21
  cities         name                              -> 8_2
  awards         long, short                       -> 8_0
A field missing (or empty) keeps the English. Three/four-letter codes are never changed.

    python tools/langdb_write.py [--he DIR] [--out FILE] [--langs 8,1000004]
    python tools/langdb_write.py --check      rebuild with no changes and compare with the original
    python tools/langdb_write.py --markers --out work/test/pack-dbnames/lang_db_he.dat
                                              in-game test copy: every in-scope todo field = '~' + English
                                              (ASCII, no Hebrew fonts needed), categories in
                                              --marker-cats (default: all); needs work/dbnames/todo
                                              (python tools/dbnames_scope.py)
"""
import argparse, glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fmf, langdb  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, 'work', 'dbnames')
HE_DIR = os.path.join(ROOT, 'translation', 'he', 'dbnames')

CATEGORY = {  # category -> (table, {he field: table field})
    'nations': ('9', {'long': 'long', 'short': 'short'}),
    'nationalities': ('9', {'m': 'nationality'}),
    'competitions': ('25', {'long': 'long', 'short': 'short', 'abbr': 'abbr'}),
    'competitions_lower': ('25', {'long': 'long', 'short': 'short', 'abbr': 'abbr'}),
    'clubs': ('3', {'long': 'long', 'short': 'short', 'abbr6': 'abbr6', 'nickname': 'nickname'}),
    'stadiums': ('21', {'name': 'name', 'alt_name': 'alt_name'}),
    'cities': ('2', {'name': 'name'}),
    'awards': ('0', {'long': 'long', 'short': 'short'}),
}
# longest English value in the shipped table (characters); Hebrew must not be longer
LIMITS = {('3', 'long'): 50, ('3', 'short'): 25, ('3', 'abbr6'): 6, ('3', 'nickname'): 39,
          ('25', 'long'): 50, ('25', 'short'): 25, ('25', 'abbr'): 4, ('9', 'long'): 32, ('9', 'short'): 25,
          ('9', 'nationality'): 25, ('21', 'name'): 50, ('21', 'alt_name'): 48, ('2', 'name'): 40,
          ('0', 'long'): 75, ('0', 'short'): 50}


def load_he(he_dir=HE_DIR):
    """{category: {db id: {he field: Hebrew}}} from translation/he/dbnames/*.json."""
    out = {}
    for p in sorted(glob.glob(os.path.join(he_dir, '*.json'))):
        out[os.path.splitext(os.path.basename(p))[0]] = {int(k): v for k, v in json.load(open(p, encoding='utf-8')).items()}
    return out


def load_done(he_dir=HE_DIR):
    """{table: {id: {table field: Hebrew}}} from translation/he/dbnames; problems as a list of strings."""
    out, problems = {}, []
    for cat, recs in load_he(he_dir).items():
        table, fmap = CATEGORY[cat]
        for i, he in recs.items():
            for hf, tf in fmap.items():
                v = (he.get(hf) or '').strip()
                if not v:
                    continue
                lim = LIMITS.get((table, tf))
                if lim and len(v) > lim:
                    problems.append(f'{cat} {i} {hf}: {len(v)} > {lim} chars, kept English')
                    continue
                out.setdefault(table, {}).setdefault(i, {})[tf] = v
    return out, problems


def load_markers(todo, cats):
    """Like load_done, from the todo batches: each field = '~' + its English (cut to the field's limit)."""
    out = {}
    for p in sorted(glob.glob(os.path.join(todo, '*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        if cats and d['category'] not in cats:
            continue
        table, fmap = CATEGORY[d['category']]
        src = {'m': 'nationality'}  # nationalities: the item's English field
        for it in d['items']:
            for hf, tf in fmap.items():
                en = it.get(src.get(hf, hf))
                if not en:
                    continue
                v = ('~' + en)[:LIMITS.get((table, tf), 99)]
                for i in it['ids']:
                    out.setdefault(table, {}).setdefault(i, {})[tf] = v
    return out, []


def patch_table(b, t, names):
    """Table bytes with the named string fields of the records in `names` ({id: {field: value}}) replaced."""
    header, recs = langdb.parse_table(b, t)
    fields = langdb.SCHEMAS[t][1]
    n = 0
    for rid, parts in recs:
        new = names.get(rid)
        if not new:
            continue
        si = 0
        for j, p in enumerate(parts):
            if isinstance(p, str):
                if si < len(fields) and fields[si] in new:
                    parts[j] = new[fields[si]]
                si += 1
        n += 1
    return langdb.join_table(header, recs), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=langdb.LANG_DB)
    ap.add_argument('--he', default=HE_DIR, help='folder of <category>.json Hebrew files')
    ap.add_argument('--out', default=os.path.join(WORK, 'build', 'lang_db_he.dat'))
    ap.add_argument('--langs', default='8', help='language ids whose tables get the Hebrew (8 = English)')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--markers', action='store_true')
    ap.add_argument('--marker-cats', default='')
    a = ap.parse_args()
    d = open(a.src, 'rb').read()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    if a.check:
        _, files, _, _ = fmf.read_index(d)
        ok, other = 0, []
        for f in files:  # every name table we write parses and re-joins to the same bytes
            t = f['name'].partition('_')[2]
            if t in langdb.SCHEMAS:
                b = fmf.read_file(d, f)
                try:
                    h, r = langdb.parse_table(b, t)
                except Exception:  # noqa: BLE001  Greek (12) has its own record layout; we never write it
                    assert not f['name'].startswith('8_'), f['name']
                    other.append(f['name'])
                    continue
                assert langdb.join_table(h, r) == b, f['name']
                ok += 1
        print(ok, 'name tables parse and re-join byte-identically; other layout (not written):', other)
        fmf.rebuild(d, {}, a.out)
        same = open(a.out, 'rb').read() == d
        print('tables round-trip; archive rebuild byte-identical:', same)
        sys.exit(0 if same else 1)
    if a.markers:
        names, problems = load_markers(os.path.join(WORK, 'todo'), [c for c in a.marker_cats.split(',') if c])
    else:
        names, problems = load_done(a.he)
    _, files, _, _ = fmf.read_index(d)
    replace = {}
    for lang in a.langs.split(','):
        for t, by_id in names.items():
            f = next(f for f in files if f['name'] == f'{lang}_{t}')
            b, n = patch_table(fmf.read_file(d, f), t, by_id)
            replace[f['name'] + f['ext']] = b
            print(f'{lang}_{t} ({langdb.TABLE_NAMES[t]}): {n} records in Hebrew')
    for p in problems:
        print('!', p)
    fmf.rebuild(d, replace, a.out)
    # read back what we wrote
    e = open(a.out, 'rb').read()
    _, f2, _, _ = fmf.read_index(e)
    for key, b in replace.items():
        f = next(f for f in f2 if f['name'] + f['ext'] == key)
        assert fmf.read_file(e, f) == b, key
    print('wrote', a.out, len(e), 'bytes')


if __name__ == '__main__':
    main()
