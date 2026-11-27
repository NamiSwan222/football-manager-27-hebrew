"""Normalises line breaks to the English form (escaped \n vs real) and appends a missing [%type#N-hidden] marker when the Hebrew dropped an argument that the English referred to
only through English pronoun variants (-you, -your, -I, -he...), as the glossary asks.

    python tools/fix_hidden.py [prefix]      rewrites work/done/<prefix>*.json in place
"""
import glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOK = re.compile(r'\[%([a-z_]+)#(\w+)(?:-([A-Za-z_]+))?\]')


GENDERED = re.compile(r'\[%person#(\w+)-(?:he|she|his|her|him|himself|herself|hers)\]', re.I)
SEX = re.compile(r'\[%(male|female)#(\w+)(-[A-Za-z_]+)?\]')


def split_people(en, he):
    """Arguments a male/female variant may mark: those the English refers to with he/she pronouns, plus any the
    Hebrew names with a visible [%male#N]/[%female#N] token."""
    out = set(GENDERED.findall(en))
    out |= {n for _, n, v in SEX.findall(he) if v != '-hidden'}
    return out


def unmark(en, he):
    """[%male#N-hidden] for an argument that is not the split person (e.g. the manager's dropped "I") -> [%person#N-hidden]."""
    ok = split_people(en, he)
    out = SEX.sub(lambda m: m.group(0) if m.group(3) != '-hidden' or m.group(2) in ok else f'[%person#{m.group(2)}-hidden]', he)
    return out if SEX.search(out) else he  # never leave a variant with no male/female marker


def fix_one(en, he, gender=None):
    BSN, NL = chr(92) + 'n', chr(10)
    if BSN in en and NL not in en and NL in he:
        he = he.replace(NL, BSN)  # the English uses the escaped line break: keep the same form
    have = check.args(he)
    add = []
    for t, n, var in TOK.findall(en):
        key = ('P' if t in check.PEOPLE else t, n)
        if key in have or key in {a for a, _ in add}:
            continue
        typ = t
        if t == 'person' and gender in ('m', 'f') and n in split_people(en, he):
            typ = 'male' if gender == 'm' else 'female'
        add.append((key, f'[%{typ}#{n}-hidden]'))
    he = he + ''.join(x for _, x in add) if add else he
    return unmark(en, he) if gender in ('m', 'f') else he


def main():
    pre = sys.argv[1] if len(sys.argv) > 1 else ''
    units = json.load(open(os.path.join(ROOT, 'work', 'en', 'units.json'), encoding='utf-8'))
    n = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'work', 'done', pre + '*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        changed = False
        for k, v in d.items():
            en = units[int(k)]['en']
            if isinstance(v, dict):
                nv = {g: fix_one(en, s, g) if isinstance(s, str) else s for g, s in v.items()}
            elif isinstance(v, str):
                nv = fix_one(en, v)
            else:
                continue
            if nv != v:
                d[k] = nv
                changed = True
                n += 1
        if changed:
            json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(n, 'units got a -hidden marker')


if __name__ == '__main__':
    main()
