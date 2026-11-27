"""FM27 English text (example.ltf) -> translation units.

    python tools/extract.py      -> work/en/units.json [{u, en, comment, keys, gender, words}],
                                    work/en/keys.json (every ltf key in file order),
                                    work/en/key_unit.json ({ltf key: unit number}, every key)

work/en/ is the player's own English, regenerated from their install and never committed. Unit numbers are
the order of first appearance in example.ltf: the same template always gives the same numbers (checked
2026-11-27), but a game patch can shift them. The tracked Hebrew, translation/he/units.json, is therefore
keyed by the unit's first ltf key ({"<key>": Hebrew | {m, f}}; a value may also be {"he": ..., "note": ...}
for our own notes); load_he() resolves those keys through key_unit.json, so any key of the unit works.

A unit is one distinct English text (`base`: used by a key without a gender suffix) (COMMENT removed); `keys` are all ltf keys using it (first 5 kept for
context, `n` = count), `comment` the first developer note, `gender` = "split" when the text refers to a
[%person#N] with English pronouns in a key without -M/-F (Hebrew then needs a male and a female variant).
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ltf  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.expandvars(r'%USERPROFILE%\Documents\Sports Interactive\Football Manager 27\languages\example.ltf')
PRONOUN = re.compile(r'\[%person#\w+-(he|she|his|her|him|himself|herself|He|She|His|Her|Him)\]')


NL = chr(10)
HE_UNITS = os.path.join(ROOT, 'translation', 'he', 'units.json')


def load_units():
    """The regenerated English units (python tools/extract.py)."""
    p = os.path.join(ROOT, 'work', 'en', 'units.json')
    if not os.path.exists(p):
        sys.exit('work/en/units.json missing: run python tools/extract.py first')
    return json.load(open(p, encoding='utf-8'))


def he_of(v):
    """A tracked value without our notes: Hebrew string or {m, f}."""
    return v['he'] if isinstance(v, dict) and 'he' in v else v


def load_he(raw=False):
    """{unit number: Hebrew | {m, f}} from translation/he/units.json, plus a list of problems (keys the
    template no longer has, two keys of one unit). raw=True keeps notes ({"he", "note"} values)."""
    key_unit = json.load(open(os.path.join(ROOT, 'work', 'en', 'key_unit.json'), encoding='utf-8'))
    tracked = json.load(open(HE_UNITS, encoding='utf-8')) if os.path.exists(HE_UNITS) else {}
    out, problems = {}, []
    for k, v in tracked.items():
        u = key_unit.get(k)
        if u is None:
            problems.append(f'key {k}: not in example.ltf any more')
        elif u in out:
            problems.append(f'key {k}: unit {u} already has Hebrew from another key')
        else:
            out[u] = v if raw else he_of(v)
    return out, problems


def save_he(tr, units):
    """Writes {unit number: value} as translation/he/units.json, keyed by each unit's first ltf key, in
    template order. Holds no English."""
    os.makedirs(os.path.dirname(HE_UNITS), exist_ok=True)
    out = {units[u]['keys'][0]: v for u, v in sorted(tr.items()) if v}
    with open(HE_UNITS, 'w', encoding='utf-8', newline=NL) as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    return len(out)


def main():
    head, entries = ltf.read(TEMPLATE)
    units, by_text, key_unit = [], {}, {}
    for key, raw in entries:
        en = ltf.plain(raw)
        m = re.search(r'\[COMMENT[:\s-]*([^\]]*)\]', raw)
        if en not in by_text:
            by_text[en] = len(units)
            units.append({'u': len(units), 'en': en, 'comment': (m.group(1).strip()[:200] if m else ''), 'keys': [], 'n': 0,
                          'gender': '', 'words': len(en.split()), 'base': False})
        u = units[by_text[en]]
        key_unit[key] = u['u']
        u['n'] += 1
        if '-' not in key:
            u['base'] = True
        if len(u['keys']) < 5:
            u['keys'].append(key)
        if '-' not in key and PRONOUN.search(en):
            u['gender'] = 'split'
    os.makedirs(os.path.join(ROOT, 'work', 'en'), exist_ok=True)
    json.dump(units, open(os.path.join(ROOT, 'work', 'en', 'units.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump([k for k, _ in entries], open(os.path.join(ROOT, 'work', 'en', 'keys.json'), 'w'))
    json.dump(key_unit, open(os.path.join(ROOT, 'work', 'en', 'key_unit.json'), 'w'))
    print(len(entries), 'entries ->', len(units), 'units,', sum(u['words'] for u in units), 'words;',
          sum(1 for u in units if u['gender']), 'need male/female variants')


if __name__ == '__main__':
    main()
