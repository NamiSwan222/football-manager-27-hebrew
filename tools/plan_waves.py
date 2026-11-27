"""Splits the FM27 units that are not in the UI pass into prioritised Sonnet batches.

    python tools/plan_waves.py [--words 50000]   -> work/todo/<tier>-NNN.json, work/waves.json

Base texts first, then texts used only by gender-variant keys (-M, -MF, ... : 'var-' tiers). Tiers (what a player sees most first): match (commentary, match day, team talks, touchline, match stats),
news (inbox, news, media, social media, transfers), press (press conferences), rest. Units keep game
order inside a tier. Units already translated (work/done/*.json) are skipped, so re-running after a crash
plans only what is left.
"""
import argparse, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIERS = [
    ('match', r'commentary|match engine|in-match|in match|half.?time|full.?time|team ?talk|touchline|match ?day|'
              r'post.?match|pre.?match|official_stats|match analysis|match report|live match|shout'),
    ('news', r'inbox|news|media|social|transfer|rumou?r|speculation|scout report|bio'),
    ('press', r'press'),
]


def is_ui(u):
    return u['words'] <= 8 and not re.search(r'\[%(person|male|female)', u['en'])


def tier_of(u):
    c = u['comment'].lower()
    for name, rx in TIERS:
        if re.search(rx, c):
            return name
    return 'rest'


def done_units():
    out = set()
    for p in glob.glob(os.path.join(ROOT, 'work', 'done', '*.json')):
        out |= {int(k) for k in json.load(open(p, encoding='utf-8'))}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--words', type=int, default=50000)
    a = ap.parse_args()
    units = json.load(open(os.path.join(ROOT, 'work', 'en', 'units.json'), encoding='utf-8'))
    done = done_units()
    plan = {}
    names = [t for t, _ in TIERS] + ['rest']
    # base texts (keys without a gender suffix) first; texts used only by gender-variant keys last
    for name in names + ['var-' + t for t in names]:
        base = not name.startswith('var-')
        tier = name[4:] if not base else name
        sel = [u for u in units if u['u'] not in done and u.get('base', True) == base
               and (base and is_ui(u) and tier == 'ui' or not is_ui(u) and tier_of(u) == tier or not base and is_ui(u) and tier == 'rest')]
        batches, cur, w = [], [], 0
        for u in sel:
            item = {'u': u['u'], 'en': u['en'], 'comment': u['comment']}
            if u['gender']:
                item['gender'] = u['gender']
            cur.append(item)
            w += u['words']
            if w >= a.words:
                batches.append(cur)
                cur, w = [], 0
        if cur:
            batches.append(cur)
        names = []
        for i, b in enumerate(batches):
            n = f'{name}-{i:03d}'
            json.dump(b, open(os.path.join(ROOT, 'work', 'todo', n + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
            names.append(n)
        plan[name] = names
        print(name, len(sel), 'units', sum(u['words'] for u in sel), 'words', len(batches), 'batches')
    json.dump(plan, open(os.path.join(ROOT, 'work', 'waves.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
