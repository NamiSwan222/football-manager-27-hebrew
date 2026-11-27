"""Removes [%type#N-hidden] markers for arguments the English text does not have (the game passes no such
argument); prints visible tokens for missing arguments so they can be fixed by hand.

    python tools/fix_extra.py [prefix]
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = re.compile(r'\[%([A-Za-z_]+)#(\w+)')
HID = re.compile(r'\[%([a-z_]+)#(\w+)-hidden\]')
P = {'person', 'male', 'female'}


def key(t, n):
    t = t.lower()
    return ('P' if t in P else t, n)


def main():
    pre = sys.argv[1] if len(sys.argv) > 1 else ''
    units = json.load(open(os.path.join(ROOT, 'work', 'en', 'units.json'), encoding='utf-8'))
    removed, visible = 0, []
    for p in glob.glob(os.path.join(ROOT, 'work', 'done', pre + '*.json')):
        d = json.load(open(p, encoding='utf-8'))
        changed = False
        for k, v in d.items():
            en = {key(t, n) for t, n in T.findall(units[int(k)]['en'])}

            def fix(s):
                nonlocal removed
                out = HID.sub(lambda m: m.group(0) if key(m.group(1), m.group(2)) in en else '', s)
                removed += s.count('-hidden]') - out.count('-hidden]')
                for t, n in T.findall(out):
                    if key(t, n) not in en:
                        visible.append((os.path.basename(p), k, t, n))
                return out
            nv = {g: fix(s) for g, s in v.items()} if isinstance(v, dict) else fix(v) if isinstance(v, str) else v
            if nv != v:
                d[k] = nv
                changed = True
        if changed:
            json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(removed, 'hidden markers removed for arguments the English lacks')
    for x in visible:
        print('visible extra token:', *x)


if __name__ == '__main__':
    main()
