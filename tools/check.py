"""Automatic check of translated FM27 batches.

    python tools/check.py <batch> [<batch> ...]     (names like ui-00, match-003)
    python tools/check.py --all

Per unit: present; every `[%type#N` argument of the English kept (as person/male/female for people);
no English pronoun variants (-he] -his] ...) or {s}/{an} helpers; Hebrew letters; not mostly Latin words;
gender-split units have both m and f. Also a few glossary term spot checks. Prints per-batch numbers and
the first problems; exit 1 if a batch has more than 1% problem units.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BSN, NL = chr(92) + 'n', chr(10)
HEB = re.compile(r'[א-ת]')
ARG = re.compile(r'\[%([a-z_]+)#(\w+)')
EN_PRON = re.compile(r'\[%\w+#\w+-(he|she|his|her|him|himself|herself|I|me|my|you|your|He|She|His|Her|Him|You|Your|My)\]')
TERMS = [('clean sheet', 'שער(ים)? נקי'), ('hat-trick', 'שלושער'), ('relegation', 'יריד|ירד|הישרדות|תחתית'),
         ('press conference', 'מסיב(ת|ות) ה?עיתונאים'), ('transfer window', 'חלון|חלונות')]
PEOPLE = {'person', 'male', 'female'}


def args(s):
    out = set()
    for t, n in ARG.findall(s):
        out.add(('P' if t in PEOPLE else t.replace('male_', '').replace('female_', ''), n))
    return out


def check_text(en, he):
    if not isinstance(he, str) or not he.strip():
        return 'empty'
    if he.strip() == en.strip() and len(en.strip()) <= 6:
        return None  # codes and symbols kept as they are (currency codes, units, acronyms)
    if EN_PRON.search(he):
        return 'English pronoun token'
    if re.search(r'\{[^}]*\|[^}]*\}', he):
        return 'invented {a|b} form'
    if re.search(r'[⟦⟧]|[א-ת]\|[א-ת]', he):
        return 'invented a|b alternative'
    if '/' not in en and re.search(r'[א-ת]/[א-ת]', he):
        return 'invented a/b alternative'
    if re.search(r'\{(s|an|An|a)\}', he):
        return 'English brace helper'
    if en.count(BSN) != he.count(BSN) or en.count(NL) != he.count(NL):
        return 'line breaks differ'
    if re.search(r'([ךםןףץ])(?!\1)[א-ת]', he):
        return 'final letter inside a word'
    miss = args(en) - args(he)
    if miss:
        return f'missing token {sorted(miss)[:3]}'
    plain = re.sub(r'\[[^\]]*\]|\{[^}]*\}|<[^>]*>', ' ', he)
    words = re.findall(r'[A-Za-zא-ת]+', plain)
    if re.search(r'[A-Za-z]{2}', re.sub(r'\[[^\]]*\]|\{[^}]*\}|<[^>]*>', '', en)) and not HEB.search(plain):
        return 'no Hebrew'
    lat = [w for w in words if re.match(r'[A-Za-z]', w) and len(w) > 2 and not w.isupper() and not w[0].isupper()]
    if words and len(lat) > 0.3 * len(words):
        return 'mostly English'
    return None


def check(batch):
    todo = json.load(open(os.path.join(ROOT, 'work', 'todo', batch + '.json'), encoding='utf-8'))
    p = os.path.join(ROOT, 'work', 'done', batch + '.json')
    if not os.path.exists(p):
        return None
    done = json.load(open(p, encoding='utf-8'))
    probs, term_hits, term_total = [], 0, 0
    for it in todo:
        h = done.get(str(it['u']))
        if h is None:
            probs.append((it['u'], 'missing'))
            continue
        if it.get('gender') == 'split':
            if not isinstance(h, dict) or not h.get('m') or not h.get('f'):
                probs.append((it['u'], 'needs m/f'))
                continue
            vals = [h['m'], h['f']]
            if '[%male#' not in h['m'] or '[%female#' not in h['f']:
                probs.append((it['u'], 'split variant without [%male#/[%female# marker'))
                continue
        else:
            vals = [h if isinstance(h, str) else (h.get('m') if isinstance(h, dict) else None)]
        for v in vals:
            why = check_text(it['en'], v)
            if why:
                probs.append((it['u'], why))
                break
        low = it['en'].lower()
        for en_t, he_t in TERMS:
            if en_t in low:
                term_total += 1
                term_hits += any(re.search(he_t, v or '') for v in vals)
    return len(todo), probs, term_hits, term_total


def main():
    names = sys.argv[1:]
    if names == ['--all']:
        names = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, 'work', 'done', '*.json')))
    bad = False
    for b in names:
        r = check(b)
        if r is None:
            print(b, 'not done')
            continue
        n, probs, th, tt = r
        rate = len(probs) / max(n, 1)
        print(f'{b}: {n} units, {len(probs)} problems ({100 * rate:.2f}%), glossary terms {th}/{tt}')
        for u, why in (probs if os.environ.get('CHECK_ALL') else probs[:8]):
            print('   ', u, why)
        bad |= rate > 0.01
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
