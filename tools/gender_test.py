"""In-game test language: every ltf entry = a marker + its English, to see which key the game prints.

    python tools/gender_test.py <out hebrew.ltf> <GENDERS 0|2> [--male-base]   write the marked language
    python tools/gender_test.py --ltc <hebrew.ltc>                     summarise what FM compiled

Markers: "^" for keys without gender variants, "0~" for the base key of a family that has variants,
"<suffix>~" for a variant (M~, F~, MF~, A~, B~...: "KEY-123-MF" -> "MF~"). Text without a marker on
screen comes from the database or the engine, not from the ltf.
"""
import collections, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ltc, ltf  # noqa: E402

TEMPLATE = os.path.expandvars(r'%USERPROFILE%\Documents\Sports Interactive\Football Manager 27\languages\example.ltf')


def build(out, genders, male_base=False):
    """male_base: the base key of a family gets "0~" + the English of its all-male variant (-M, -MM...),
    i.e. [%male#N] tokens instead of [%person#N]. If the engine picks the first variant whose gender
    tokens fit, a female then gets the F~ (MF~/FM~/FF~) text and a male the 0~ text."""
    _, entries = ltf.read(TEMPLATE)
    family = {k.split('-')[0] for k, _ in entries if '-' in k}
    male = {}
    for key, en in entries:
        base, _, suf = key.partition('-')
        if suf and set(suf) == {'M'}:
            male.setdefault(base, ltf.plain(en))
    tr = {}
    for key, en in entries:
        base, _, suf = key.partition('-')
        mark = f'{suf}~' if suf else ('0~' if base in family else '^')
        text = male.get(base, ltf.plain(en)) if male_base and not suf else ltf.plain(en)
        tr[key] = mark + text.replace('\n', '\\n')  # FM keeps only the first line of an STR
    ltf.write(out, 'Hebrew', entries, tr, genders=genders)
    print(len(entries), 'entries written to', out, 'GENDERS', genders, 'male base' if male_base else '')


def summary(path):
    d = ltc.read(path)
    print(d['name'], len(d['strings']), 'records;', 'variant records by size:',
          dict(collections.Counter(len(v) for v in d['variants'].values())))
    marks = collections.Counter(s.split('~', 1)[0] if '~' in s[:8] else s[:1] for s in d['strings'])
    print('first-variant markers:', marks.most_common(12))
    for i, vs in list(d['variants'].items())[:8]:
        print(' ', [v[:70] for v in vs])


if __name__ == '__main__':
    if sys.argv[1] == '--ltc':
        summary(sys.argv[2])
    else:
        build(sys.argv[1], int(sys.argv[2]), '--male-base' in sys.argv)
