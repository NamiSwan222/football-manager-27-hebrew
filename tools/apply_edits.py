"""Apply Opus edits (work/edit/<batch>.json, changed units only) onto work/done/<batch>.json.

    python tools/apply_edits.py <batch> [...]

An edit is applied only if it passes the same checks as tools/check.py; rejected edits are listed.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    for b in sys.argv[1:]:
        ep = os.path.join(ROOT, 'work', 'edit', b + '.json')
        dp = os.path.join(ROOT, 'work', 'done', b + '.json')
        edits = json.load(open(ep, encoding='utf-8'))
        done = json.load(open(dp, encoding='utf-8'))
        todo = {str(x['u']): x for x in json.load(open(os.path.join(ROOT, 'work', 'todo', b + '.json'), encoding='utf-8'))}
        ok = bad = 0
        for k, v in edits.items():
            it = todo.get(k)
            if it is None:
                bad += 1
                continue
            vals = [v['m'], v['f']] if isinstance(v, dict) else [v]
            why = next((w for w in (check.check_text(it['en'], s) for s in vals) if w), None)
            if why:
                bad += 1
                print('  rejected', k, why)
                continue
            done[k] = v
            ok += 1
        json.dump(done, open(dp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print(b, 'applied', ok, 'rejected', bad)


if __name__ == '__main__':
    main()
