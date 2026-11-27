"""After re-extraction: carry translations from work/done_old (old unit numbers, work/en/units.old.json)
to the new units by English text. Old units that had merged "KEY-<id>-XX:" lines are split per line.

    python tools/carry.py   -> work/done/carried.json + work/todo/carried.json
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYLINE = re.compile(r'\nKEY-\d+(?:-[A-Z]+)?: ?')


def parts(s):
    return KEYLINE.split(s)


def main():
    old = json.load(open(os.path.join(ROOT, 'work', 'en', 'units.old.json'), encoding='utf-8'))
    new = json.load(open(os.path.join(ROOT, 'work', 'en', 'units.json'), encoding='utf-8'))
    by_en = {}
    skipped = 0
    for p in glob.glob(os.path.join(ROOT, 'work', 'done_old', '*.json')):
        for k, he in json.load(open(p, encoding='utf-8')).items():
            en = old[int(k)]['en']
            ens = parts(en)
            if isinstance(he, dict):
                hs = {g: parts(v) for g, v in he.items()}
                if all(len(v) == len(ens) for v in hs.values()):
                    for i, e in enumerate(ens):
                        by_en[e.strip()] = {g: v[i].strip() for g, v in hs.items()}
                else:
                    skipped += 1
                continue
            hl = parts(he)
            if len(hl) != len(ens):
                skipped += 1
                continue
            for e, h in zip(ens, hl):
                by_en[e.strip()] = h.strip()
    done, todo = {}, []
    for u in new:
        h = by_en.get(u['en'].strip())
        if h is None:
            continue
        if u['gender'] == 'split' and not isinstance(h, dict):
            continue  # needs m/f now
        if u['gender'] != 'split' and isinstance(h, dict):
            h = h.get('m')
        done[str(u['u'])] = h
        item = {'u': u['u'], 'en': u['en'], 'comment': u['comment']}
        if u['gender']:
            item['gender'] = u['gender']
        todo.append(item)
    json.dump(done, open(os.path.join(ROOT, 'work', 'done', 'carried.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    json.dump(todo, open(os.path.join(ROOT, 'work', 'todo', 'carried.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(by_en), 'English texts translated;', len(done), 'new units carried;', skipped, 'old units not splittable')


if __name__ == '__main__':
    main()
