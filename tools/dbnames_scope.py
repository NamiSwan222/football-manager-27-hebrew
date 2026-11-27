"""FM27 Hebrew DB names: decide which records get Hebrew, and write Sonnet work batches.

Reads (never writes) the game's database: server_db.dat (main data) and lang_db.dat (English names, table
schemas in tools/langdb.py). What the main database gives us (worked out 2026-11-26, files only):

- Every server table is `03 01 'dat.' u16 0x0fa0, u32 count`, then records in the same order as the lang
  tables (record k of server table_3 = record k of lang 8_3), each record ending with `u32 row, u32 id,
  u32 id`. That trailer is how records are split here (the fields in between are not decoded).
  Cross-references inside records are ROW numbers (not db ids).
- table_3 (clubs): record starts `u8, u32 nation, ...`; u32 @13 = nation row, u32 @17 = city row.
- table_24 (teams: 100,930 = clubs + national teams, trailer id = club / nation db id): first byte 0x0a club,
  0x0b national team; u16 @3 = reputation, u32 @5 = current division (comp row, -1 = none), u32 @9 = last
  division, u32 @17 = stadium row.
- table_25 (comps): u16 @16 = level (0 top division, 1 second, ..., 100 = cup/other; row 0 has one extra
  leading byte); nation row = the u32 after `u16 year, u16, u16 year, u32 n<16` in bytes 40..120
  (0xFFFFFFFF = continental / international).
- Women's clubs have db ids >= 2,000,000,000.

"Default playable nations" is not a field we found: it is the PLAYABLE list below (FM26/FM27 playable
league nations, men's), plus WOMEN_PLAYABLE for the women's pyramid. Edit them and rerun.

    python tools/dbnames_scope.py              -> work/dbnames/scope.json, todo/<category>-NNN.json, counts
"""
import json, os, pickle, re, struct, sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fmf, langdb  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, 'work', 'dbnames')
CACHE = os.path.join(WORK, 'cache')
SERVER_DB = os.path.join(os.path.dirname(langdb.LANG_DB), 'server_db.dat')

PLAYABLE = [
    'Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Bulgaria', 'Chile', 'China PR', 'Colombia',
    'Croatia', 'Czechia', 'Denmark', 'England', 'Finland', 'France', 'Germany', 'Greece',
    'Hong Kong (China PR)', 'Hungary', 'India', 'Indonesia', 'Israel', 'Italy', 'Japan', 'Malaysia', 'Mexico',
    'Netherlands', 'Northern Ireland', 'Norway', 'Peru', 'Poland', 'Portugal', 'Republic of Ireland',
    'Romania', 'Russia', 'Saudi Arabia', 'Scotland', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia',
    'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Türkiye', 'Ukraine', 'United States',
    'Uruguay', 'Wales',
]
WOMEN_PLAYABLE = ['England', 'United States', 'Spain', 'France', 'Germany', 'Italy', 'Sweden', 'Netherlands',
                  'Australia', 'Scotland', 'Brazil', 'Mexico', 'Japan', 'Norway', 'Denmark']
WOMEN_ID = 2_000_000_000
YOUTH = re.compile(r'\b(U-?\d\d|Under[- ]\d\d|Youth|Reserve|Reserves|Academy|Juniors?|Development|Premier League 2|B Teams?|'
                   r'M-League|President Cup|Elite Youth)\b', re.I)
WOMEN = re.compile(r"\bWomen|Ladies|Frauen|Femenin|Féminin|Feminin|Damallsvenskan|Elitettan|Arkema|WE League", re.I)
# season years (u16 0x07xx), u16, u16 year, u32 small, u32 nation row
NAT_RE = re.compile(rb'.\x07...\x07[\x00-\x10]\x00\x00\x00(.{4})', re.S)
BATCH = {'nations': 40, 'competitions': 60, 'competitions_lower': 80, 'clubs': 60, 'stadiums': 80, 'cities': 100, 'awards': 60}


def split_records(b, ids, name):
    """[(start, end)] of every record, found by its `row, id, id` trailer (cached)."""
    p = os.path.join(CACHE, name + '.pkl')
    if os.path.exists(p):
        return pickle.load(open(p, 'rb'))
    o, out = 12, []
    for k, rid in enumerate(ids):
        j = b.find(struct.pack('<III', k, rid, rid), o)
        assert j >= 0, (name, k, rid)
        out.append((o, j + 12))
        o = j + 12
    os.makedirs(CACHE, exist_ok=True)
    pickle.dump(out, open(p, 'wb'))
    return out


def split_teams(b):
    """table_24 has no lang twin: ids are found as `row, a, a` followed by a record starting 0x0a/0x0b."""
    p = os.path.join(CACHE, 'teams.pkl')
    if os.path.exists(p):
        return pickle.load(open(p, 'rb'))
    n, o, out = struct.unpack_from('<I', b, 8)[0], 12, []
    for k in range(n):
        j = b.find(struct.pack('<I', k), o)
        while True:
            a, c = struct.unpack_from('<II', b, j + 4)
            if a == c and a != 0xFFFFFFFF and (j + 12 >= len(b) - 16 or b[j + 12] in (0x0A, 0x0B)):
                break
            j = b.find(struct.pack('<I', k), j + 1)
        out.append((o, j + 12, a))
        o = j + 12
    pickle.dump(out, open(p, 'wb'))
    return out


def load():
    d, files = langdb.tables()
    en = {}
    for t in langdb.SCHEMAS:
        _, recs = langdb.parse_table(langdb.table(d, files, f'8_{t}'), t)
        en[t] = [dict(id=i, **langdb.fields(p, t)) for i, p in recs]
    other = {}
    for lang in ('10', '24', '11'):  # French, Spanish, German: gendered forms and exonyms as hints
        for t in ('9', '25', '2'):
            _, recs = langdb.parse_table(langdb.table(d, files, f'{lang}_{t}'), t)
            other[(lang, t)] = {i: langdb.fields(p, t) for i, p in recs}
    s = open(SERVER_DB, 'rb').read()
    _, sf, _, _ = fmf.read_index(s)
    get = lambda n: fmf.read_file(s, next(f for f in sf if f['name'] == n))
    return en, other, get('table_3'), get('table_24'), get('table_25')


def main():
    en, other, clubs_b, teams_b, comps_b = load()
    nat, comps, clubs, stad, city = en['9'], en['25'], en['3'], en['21'], en['2']
    nrow = {r['long']: k for k, r in enumerate(nat)}
    missing = [n for n in PLAYABLE + WOMEN_PLAYABLE if n not in nrow]
    assert not missing, missing

    crec = split_records(clubs_b, [r['id'] for r in clubs], 'clubs')
    club_nat = [struct.unpack_from('<i', clubs_b, s + 13)[0] for s, _ in crec]
    club_city = [struct.unpack_from('<i', clubs_b, s + 17)[0] for s, _ in crec]
    club_row = {r['id']: k for k, r in enumerate(clubs)}

    comp_level, comp_nat = [], []
    for k, (s, e) in enumerate(split_records(comps_b, [r['id'] for r in comps], 'comps')):
        s0 = s + (1 if k == 0 else 0)
        comp_level.append(struct.unpack_from('<H', comps_b, s0 + 16)[0])
        m = NAT_RE.search(comps_b, s0 + 40, min(e, s0 + 120))
        comp_nat.append(struct.unpack('<i', m.group(1))[0] if m else None)

    team = {}  # club row -> (division row, last division row, stadium row, reputation)
    for s, e, tid in split_teams(teams_b):
        if teams_b[s] == 0x0A and tid in club_row:
            rep, = struct.unpack_from('<H', teams_b, s + 3)
            div, last = struct.unpack_from('<ii', teams_b, s + 5)
            st, = struct.unpack_from('<i', teams_b, s + 17)
            team[club_row[tid]] = (div, last, st, rep)

    members = defaultdict(list)
    for k, (div, last, st, rep) in team.items():
        if div >= 0:
            members[div].append(k)

    def nation_of_comp(c):
        if comp_nat[c] is not None:
            return comp_nat[c]
        cnt = Counter(club_nat[k] for k in members[c])
        return cnt.most_common(1)[0][0] if cnt else None

    men = {nrow[n] for n in PLAYABLE}
    women = {nrow[n] for n in WOMEN_PLAYABLE}
    israel = nrow['Israel']

    # top two divisions: comps used as a division, level 0 or 1, not youth/reserve, by men's/women's clubs
    top2, top2_info = set(), []
    for c, ks in members.items():
        if comp_level[c] > 1 or YOUTH.search(comps[c]['long']) or len(ks) < 4:
            continue
        n = nation_of_comp(c)
        w = sum(clubs[k]['id'] >= WOMEN_ID for k in ks) > len(ks) / 2 or bool(WOMEN.search(comps[c]['long']))
        if (n in women if w else n in men):
            top2.add(c)
            top2_info.append((nat[n]['long'] if n >= 0 else '-', 'women' if w else 'men', comp_level[c] + 1, comps[c]['long'], len(ks)))

    club_scope = set()
    for c in top2:
        club_scope.update(members[c])
    club_scope.update(k for k in range(len(clubs)) if club_nat[k] == israel and clubs[k]['long'])

    # competitions a player can see: every comp of a playable nation + continental/international ones
    # A = top two divisions, cups/super cups/play-offs (level 100) and continental/international comps;
    # B = everything else of a playable nation (lower and regional divisions, youth, reserve, women's lower)
    comp_scope, comp_kind, comp_tier, unknown = set(), {}, {}, []
    for c in range(len(comps)):
        n = nation_of_comp(c)
        if n is None:  # no nation field found and no member clubs: world-wide comps (friendlies, Club World Cup...)
            unknown.append(comps[c]['long'])
        if n is None or n == -1:
            comp_scope.add(c); comp_kind[c] = 'international'
            comp_tier[c] = 'B' if YOUTH.search(comps[c]['long']) else 'A'
        elif n in men or n in women:
            comp_scope.add(c); comp_kind[c] = 'domestic'
            low = YOUTH.search(comps[c]['long']) or (WOMEN.search(comps[c]['long']) and n not in women)
            comp_tier[c] = 'A' if c in top2 or (comp_level[c] >= 100 and not low) else 'B'

    stad_scope = {team[k][2] for k in club_scope if k in team and team[k][2] >= 0}
    city_scope = {club_city[k] for k in club_scope if club_city[k] >= 0}

    scope = dict(
        playable_men=PLAYABLE, playable_women=WOMEN_PLAYABLE,
        top2=sorted(top2_info),
        nations=[r['id'] for r in nat], awards=[r['id'] for r in en['0']],
        competitions=sorted(comps[c]['id'] for c in comp_scope if comp_tier[c] == 'A'),
        competitions_lower=sorted(comps[c]['id'] for c in comp_scope if comp_tier[c] == 'B'),
        clubs=sorted(clubs[k]['id'] for k in club_scope),
        stadiums=sorted(stad[s]['id'] for s in stad_scope),
        cities=sorted(city[c]['id'] for c in city_scope),
    )
    os.makedirs(WORK, exist_ok=True)
    json.dump(scope, open(os.path.join(WORK, 'scope.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # ---- work items (grouped by identical English, so a name shared by many records is translated once)
    fr_n, es_n, de_n = other[('10', '9')], other[('24', '9')], other[('11', '9')]
    fr_c, fr_ci = other[('10', '25')], other[('10', '2')]
    nname = lambda n: nat[n]['long'] if n is not None and 0 <= n < len(nat) else None
    items = defaultdict(list)
    for r in nat:
        items['nations'].append(dict(ids=[r['id']], long=r['long'], short=r['short'], three=r['three'],
                                     hint_fr=fr_n.get(r['id'], {}).get('long'), hint_de=de_n.get(r['id'], {}).get('long')))
        f = fr_n.get(r['id'], {})
        items['nationalities'].append(dict(ids=[r['id']], nation=r['long'], nationality=r['nationality'],
                                           hint_fr_forms=f.get('forms'), hint_es_forms=es_n.get(r['id'], {}).get('forms')))
    for c in sorted(comp_scope, key=lambda c: (comp_kind[c], nname(nation_of_comp(c)) or '', comp_level[c], c)):
        r = comps[c]
        items['competitions' if comp_tier[c] == 'A' else 'competitions_lower'].append(dict(ids=[r['id']], long=r['long'], short=r['short'], abbr=r['abbr'],
                                          nation=nname(nation_of_comp(c)) if nation_of_comp(c) not in (None, -1) else 'international',
                                          level=comp_level[c] + 1 if comp_level[c] < 100 else 'cup/other',
                                          hint_fr=fr_c.get(r['id'], {}).get('long')))
    group = {}
    for k in sorted(club_scope, key=lambda k: (nname(club_nat[k]) or '', -team.get(k, (0, 0, 0, 0))[3])):
        r = clubs[k]
        key = (r['long'], r['short'], r['nickname'])
        if key in group:
            group[key]['ids'].append(r['id']); continue
        div = team.get(k, (-1,))[0]
        it = dict(ids=[r['id']], long=r['long'], short=r['short'], abbr6=r['abbr6'], nickname=r['nickname'],
                  nation=nname(club_nat[k]), division=comps[div]['long'] if div >= 0 else None,
                  women=r['id'] >= WOMEN_ID, city=city[club_city[k]]['name'] if club_city[k] >= 0 else None)
        group[key] = it
        items['clubs'].append(it)
    stad_users = defaultdict(list)
    for k in club_scope:
        if k in team and team[k][2] >= 0:
            stad_users[team[k][2]].append(clubs[k]['short'])
    for s in sorted(stad_scope):
        r = stad[s]
        items['stadiums'].append(dict(ids=[r['id']], name=r['name'], alt_name=r['alt_name'], clubs=sorted(set(stad_users[s]))[:4]))
    city_nat = {}
    for k in club_scope:
        city_nat.setdefault(club_city[k], nname(club_nat[k]))
    for c in sorted(city_scope, key=lambda c: (city_nat.get(c) or '', city[c]['name'])):
        r = city[c]
        items['cities'].append(dict(ids=[r['id']], name=r['name'], nation=city_nat.get(c), hint_fr=fr_ci.get(r['id'], {}).get('name')))
    group = {}
    for r in en['0']:
        key = (r['long'], r['short'])
        if key in group:
            group[key]['ids'].append(r['id']); continue
        group[key] = dict(ids=[r['id']], long=r['long'], short=r['short'])
        items['awards'].append(group[key])

    todo = os.path.join(WORK, 'todo')
    os.makedirs(todo, exist_ok=True)
    for f in os.listdir(todo):
        os.remove(os.path.join(todo, f))
    batches = {}
    for cat, lst in items.items():
        size = BATCH.get(cat, 60)
        for i in range(0, len(lst), size):
            p = os.path.join(todo, f'{cat}-{i // size:03d}.json')
            body = ',\n'.join(json.dumps(it, ensure_ascii=False) for it in lst[i:i + size])  # one item per line
            open(p, 'w', encoding='utf-8').write(f'{{"category": "{cat}", "items": [\n{body}\n]}}\n')
        batches[cat] = (len(lst), (len(lst) + size - 1) // size)

    kinds = Counter((comp_kind[c], comp_tier[c]) for c in comp_scope)
    print('top-two divisions:', len(top2), '| men', sum(1 for x in top2_info if x[1] == 'men'),
          'women', sum(1 for x in top2_info if x[1] == 'women'))
    print('records in scope: nations', len(nat), '| competitions', len(comp_scope), sorted(kinds.items()),
          '| clubs', len(club_scope), '| stadiums', len(stad_scope), '| cities', len(city_scope), '| awards', len(en['0']))
    print('competitions with no nation found (taken as international):', len(unknown), unknown[:8])
    for cat, (n, b) in batches.items():
        print(f'  {cat:14} {n:6} items  {b:4} batches')


if __name__ == '__main__':
    main()
