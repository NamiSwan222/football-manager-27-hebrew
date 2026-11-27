"""The 100% check for the FM27 Hebrew pack. Exit 0 only when everything below passes.

    python tools/coverage.py [--list] [--no-ltf]

English comes only from the player's install: work/en/units.json (python tools/extract.py, from example.ltf)
and work/dbnames/todo (python tools/dbnames_scope.py, from the game's lang_db.dat / server_db.dat). The
tracked translation/ holds Hebrew only.

0. Every key of translation/he/units.json is a key of example.ltf, one per unit.
1. Every base key (a template family whose English is not empty) has Hebrew in translation/he/units.json
   (split units: both m and f).
2. Every token argument of the English ([%type#N], people as person/male/female) is kept in the Hebrew
   (each of m and f), and the number of line breaks is the same.
3. The built work/pack/files/tirgumim/he/hebrew.ltf, compiled the way FM compiles it (tools/ltc_write.py),
   gives exactly the texts tools/build.py planned for every key; the same for hebrew.ltc if it was built.
   (Skipped with --no-ltf.) Split units' m texts carry a [%male#, f texts a [%female# token.
4. DB names: every db id of every item of every work/dbnames/todo batch has Hebrew in
   translation/he/dbnames/<category>.json in each required field (where the English has a value), within the
   field's length limit (else langdb_write keeps English).
   A name that should stay as it is (brand names like NXGN) is written into `he` as is; an absent or empty
   field counts as not done.
--list prints every problem instead of the first ten per check.
"""
import collections, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check, extract, langdb_write, ltc_write, ltf  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, 'work', 'dbnames')
NL, BSN = chr(10), chr(92) + 'n'

# he fields that must be there when the item's English field (second) has a value
REQUIRED = {
    'nations': [('long', 'long'), ('short', 'short')],
    'nationalities': [('m', 'nationality')],
    'competitions': [('long', 'long'), ('short', 'short')],
    'competitions_lower': [('long', 'long'), ('short', 'short')],
    'clubs': [('long', 'long'), ('short', 'short')],
    'stadiums': [('name', 'name'), ('alt_name', 'alt_name')],
    'cities': [('name', 'name')],
    'awards': [('long', 'long'), ('short', 'short')],
}
ORDER = list(REQUIRED)


def dbnames():
    """{category: {items, items_done, ids, ids_done, batches, batches_done, problems: [...]}}"""
    out = {c: dict(items=0, items_done=0, ids=0, ids_done=0, batches=0, batches_done=0, problems=[]) for c in ORDER}
    todo_files = sorted(glob.glob(os.path.join(DB, 'todo', '*.json')))
    if not todo_files:
        out[ORDER[0]]['problems'].append('work/dbnames/todo is empty: run python tools/dbnames_scope.py')
    he_all = langdb_write.load_he()
    for p in todo_files:
        name = os.path.basename(p)
        todo = json.load(open(p, encoding='utf-8'))
        cat = todo['category']
        c, he_cat = out[cat], he_all.get(cat, {})
        table, fmap = langdb_write.CATEGORY[cat]
        c['batches'] += 1
        c['items'] += len(todo['items'])
        c['ids'] += sum(len(it['ids']) for it in todo['items'])
        batch_done = True
        for it in todo['items']:
            bad = []
            for i in it['ids']:
                he = he_cat.get(i)
                if he is None:
                    bad.append(f'id {i} has no Hebrew')
                    continue
                for hf, ef in REQUIRED[cat]:
                    if not (it.get(ef) or '').strip():
                        continue
                    v = (he.get(hf) or '').strip()
                    lim = langdb_write.LIMITS.get((table, fmap.get(hf, hf)))
                    if not v:
                        bad.append(f'id {i} {hf} missing')
                    elif lim and len(v) > lim:
                        bad.append(f'id {i} {hf} {len(v)} > {lim} chars')
            if bad:
                batch_done = False
                c['problems'].append(f'{name} {it["ids"][0]} {it.get("long") or it.get("name") or it.get("nationality")}: '
                                     + ', '.join(sorted(set(bad))[:4]))
            else:
                c['items_done'] += 1
                c['ids_done'] += len(it['ids'])
        c['batches_done'] += batch_done
    return out


def print_dbnames(r):
    print(f'  {"category":20} {"batches":>9} {"items":>15} {"records":>15}')
    for c, v in r.items():
        pct = 100 * v['items_done'] / max(v['items'], 1)
        print(f'  {c:20} {v["batches_done"]:4}/{v["batches"]:<4} {v["items_done"]:6}/{v["items"]:<6} {v["ids_done"]:6}/{v["ids"]:<6}'
              f' {pct:6.1f}%')


def main():
    full = '--list' in sys.argv
    import build
    entries = ltf.read(build.TEMPLATE)[1]
    uid, tr = build.load_units()
    problems = collections.defaultdict(list)
    problems['0 tracked key not in the template'] = extract.load_he()[1]

    # 1 + 2: units of base keys
    base_units = {}
    for k, en in entries:
        if '-' not in k and ltc_write.fm_text(en):
            base_units.setdefault(uid[ltf.plain(en)], k)
    units = extract.load_units()
    for u, k in base_units.items():
        en, he = units[u]['en'], tr.get(u)
        if not he:
            problems['1 base key without Hebrew'].append(f'{k} (unit {u}): {en[:80]}')
            continue
        if isinstance(he, dict):
            if not he.get('m') or not he.get('f'):
                problems['1 base key without Hebrew'].append(f'{k} (unit {u}): split without m or f')
                continue
            vals = [he['m'], he['f']]
        else:
            vals = [he]
        for v in vals:
            miss = check.args(en) - check.args(v)
            if miss:
                problems['2 token argument missing'].append(f'{k} (unit {u}): {sorted(miss)}')
                break
            if en.count(BSN) + en.count(NL) != v.count(BSN) + v.count(NL):
                problems['2 line breaks differ'].append(f'{k} (unit {u})')
                break

    # 3: the built files
    if '--no-ltf' not in sys.argv:
        he_dir = build.HE
        ltf_path = os.path.join(he_dir, 'hebrew.ltf')
        if not os.path.exists(ltf_path):
            problems['3 built files'].append('hebrew.ltf not built (python tools/build.py)')
        else:
            rtl = json.load(open(os.path.join(ROOT, 'work', 'pack', 'report.json'), encoding='utf-8')).get('rtl', 'rli')
            strs, recs, _, _, _ = build.plan(entries, uid, tr, rtl)
            comp = ltc_write.compile_ltf(ltf_path)
            got = {i: comp['records'][n] for i, n, _ in comp['index']}
            fam = collections.OrderedDict()
            for k, en in entries:
                if k in strs:
                    fam.setdefault(k.split('-')[0], []).append((k, en))
            for b, es in fam.items():
                es.sort(key=lambda e: '-' in e[0])
                want = [strs[k] if strs[k] else ltc_write.fm_text(ltf.plain(en)) for k, en in es]
                have = got.get(ltc_write.ID_BASE + int(b))
                if have != want:
                    problems['3 compiled ltf differs from the plan'].append(f'{b}: {str(have)[:120]} != {str(want)[:120]}')
            if len(got) != len(fam):
                problems['3 compiled ltf differs from the plan'].append(f'{len(got)} records, {len(fam)} families')
            print(f'hebrew.ltf compiled like FM: {len(got):,} records, '
                  f'{len(problems["3 compiled ltf differs from the plan"])} differ from the plan')
            for rid, r in recs.items():
                if len(r) == 2 and ('[%male#' not in r[0] or '[%female#' not in r[1]):
                    problems['3 split record without gender tokens'].append(str(rid - ltc_write.ID_BASE))
            ltc_path = os.path.join(he_dir, 'hebrew.ltc')
            if os.path.exists(ltc_path):
                c = ltc_write.parse(ltc_path)
                if c['source_size'] != os.path.getsize(ltf_path):
                    problems['3 hebrew.ltc'].append('header source size is not the size of hebrew.ltf')
                if os.path.getmtime(ltc_path) <= os.path.getmtime(ltf_path):
                    problems['3 hebrew.ltc'].append('not newer than hebrew.ltf')
                have = {i: c['records'][n] for i, n, _ in c['index']}
                if have != recs:
                    problems['3 hebrew.ltc'].append(f'records differ from the plan ({len(have)} vs {len(recs)})')

    # 4: DB names
    db = dbnames()
    for cat, v in db.items():
        for p in v['problems']:
            problems['4 DB names ' + cat].append(p)
        if v['items_done'] < v['items']:
            problems['4 DB names ' + cat].insert(0, f'{v["items_done"]}/{v["items"]} items done')

    print(f'base keys: {len(base_units):,} units checked')
    print('DB names:')
    print_dbnames(db)
    problems = {k: v for k, v in problems.items() if v}  # a check that only looked at a key leaves an empty list
    if not problems:
        print('COVERAGE 100%: all checks pass')
        return 0
    for name, lst in sorted(problems.items()):
        print(f'{name}: {len(lst)}')
        for p in (lst if full else lst[:10]):
            print('   ', p)
    return 1


if __name__ == '__main__':
    sys.exit(main())
