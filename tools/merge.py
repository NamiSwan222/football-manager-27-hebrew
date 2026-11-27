"""Merge translated batches into the tracked Hebrew (no English is ever written to translation/).

    python tools/merge.py [batch ...]     work/done/*.json ({unit: Hebrew | {m, f}}) -> translation/he/units.json
    python tools/merge.py --dbnames       work/dbnames/done/*.json -> translation/he/dbnames/<category>.json

Units: batch keys are unit numbers from tools/extract.py (work/en/units.json); the tracked file is keyed by
each unit's first ltf key (see extract.py). Only batches listed in work/merged.txt are merged (batches still
being written are skipped); names given on the command line are added to that list first, after they passed
the fix/unify/check pipeline. Units already in the tracked file and not in a merged batch are kept, our own
notes too.

DB names: each done batch item's `he` object is written for every db id of the item, as
{"<id>": {field: Hebrew}}; the English stays in the game's lang_db.dat (tools/langdb_write.py reads it there).
"""
import glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_HE = os.path.join(ROOT, 'translation', 'he', 'dbnames')


def merge_units(names):
    units = extract.load_units()
    lst = os.path.join(ROOT, 'work', 'merged.txt')
    ok = set(open(lst, encoding='utf-8').read().split()) if os.path.exists(lst) else set()
    ok |= set(names)
    open(lst, 'w', encoding='utf-8').write('\n'.join(sorted(ok)) + '\n')
    out, problems = extract.load_he(raw=True)
    for p in problems:
        print('!', p)
    for p in sorted(glob.glob(os.path.join(ROOT, 'work', 'done', '*.json'))):
        if os.path.splitext(os.path.basename(p))[0] not in ok:
            continue
        for k, v in json.load(open(p, encoding='utf-8')).items():
            if v:
                old = out.get(int(k))
                out[int(k)] = dict(old, he=v) if isinstance(old, dict) and 'he' in old else v
    n = extract.save_he(out, units)
    print(n, 'of', len(units), 'units translated')


def merge_dbnames():
    cats = {}
    for p in sorted(glob.glob(os.path.join(DB_HE, '*.json'))):
        cats[os.path.splitext(os.path.basename(p))[0]] = json.load(open(p, encoding='utf-8'))
    n = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'work', 'dbnames', 'done', '*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        c = cats.setdefault(d['category'], {})
        for it in d['items']:
            he = {k: v for k, v in (it.get('he') or {}).items() if v}
            if he:
                for i in it['ids']:
                    c[str(i)] = he
                    n += 1
    os.makedirs(DB_HE, exist_ok=True)
    for cat, c in cats.items():
        with open(os.path.join(DB_HE, cat + '.json'), 'w', encoding='utf-8', newline='\n') as f:
            body = ',\n'.join(f'{json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}'
                              for k, v in sorted(c.items(), key=lambda x: int(x[0])))  # one record per line
            f.write('{\n' + body + '\n}\n')
        print(f'{cat:20} {len(c):6} records')
    print(n, 'records from work/dbnames/done')


if __name__ == '__main__':
    if sys.argv[1:] == ['--dbnames']:
        merge_dbnames()
    else:
        merge_units(sys.argv[1:])
