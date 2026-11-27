"""Restores the letter case of token variants to the English form ([%person#3-first] -> [%person#3-First] when the
English writes -First); translators sometimes lower-case them.

    python tools/fix_case.py [prefix]      rewrites work/done/<prefix>*.json in place
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOK = re.compile(r'\[%([a-z_]+)#(\w+)-([A-Za-z_]+)\]')


def main():
    pre = sys.argv[1] if len(sys.argv) > 1 else ''
    units = json.load(open(os.path.join(ROOT, 'work', 'en', 'units.json'), encoding='utf-8'))
    tot = 0
    for p in glob.glob(os.path.join(ROOT, 'work', 'done', pre + '*.json')):
        d = json.load(open(p, encoding='utf-8'))
        changed = False
        for k, v in d.items():
            want = {(n, var.lower()): var for t, n, var in TOK.findall(units[int(k)]['en']) if var != var.lower()}
            if not want:
                continue

            def fix(s):
                return TOK.sub(lambda m: '[%{}#{}-{}]'.format(m.group(1), m.group(2), want.get((m.group(2), m.group(3)), m.group(3))), s)
            nv = {g: fix(s) for g, s in v.items()} if isinstance(v, dict) else fix(v) if isinstance(v, str) else v
            if nv != v:
                d[k] = nv
                changed = True
                tot += 1
        if changed:
            json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(tot, 'units: token variant case restored')


if __name__ == '__main__':
    main()
