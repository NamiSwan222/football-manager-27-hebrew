"""Which glossary spot-check terms the translated batches miss, with examples.

    python tools/term_report.py [prefix]      (e.g. ui)
"""
import collections, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pre = sys.argv[1] if len(sys.argv) > 1 else ''
miss, ex = collections.Counter(), collections.defaultdict(list)
for p in glob.glob(os.path.join(ROOT, 'work', 'done', pre + '*.json')):
    b = os.path.basename(p)[:-5]
    todo = json.load(open(os.path.join(ROOT, 'work', 'todo', b + '.json'), encoding='utf-8'))
    done = json.load(open(p, encoding='utf-8'))
    for it in todo:
        h = done.get(str(it['u']))
        if not isinstance(h, str):
            continue
        for en_t, he_t in check.TERMS:
            if en_t in it['en'].lower() and not re.search(he_t, h):
                miss[en_t] += 1
                if len(ex[en_t]) < 5:
                    ex[en_t].append((it['en'][:60], h[:60]))
print(miss)
for k, v in ex.items():
    print(k)
    for e in v:
        print('   ', e)
