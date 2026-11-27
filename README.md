# Football Manager 27: Hebrew translation (work in progress)

Steam app 4530370, `D:\SteamLibrary\steamapps\common\Football Manager 27`, Unity 6 UI (IL2CPP) + Sports
Interactive's native engine `fm_Data\Plugins\x86_64\game_plugin.dll` (400 MB, anti-tamper protected).

## Repository layout: Hebrew only (2026-11-27)

The repo never holds the game's English (GAMES.md rule 4). Tracked:
- `translation/he/units.json`: `{"<first ltf key of the unit>": Hebrew | {"m", "f"}}` (a value may also be
  `{"he": ..., "note": ...}` for our own notes). Units are the distinct English texts of `example.ltf`, numbered
  in order of first appearance (deterministic for one template); the tracked file is keyed by ltf key so it
  survives a re-extract, and `tools/extract.py` `load_he()` maps any key of a unit back to its number.
- `translation/he/dbnames/<category>.json`: `{"<db id>": {field: Hebrew}}` for nations, nationalities,
  competitions, competitions_lower, clubs, stadiums, cities, awards.
- tools, docs (glossaries and translator instructions with short English terms), fonts, `pack/`.

Regenerated from the player's own install and gitignored (`work/`): `python tools/extract.py` ->
`work/en/units.json`, `keys.json`, `key_unit.json` (English units); `python tools/dbnames_scope.py` ->
`work/dbnames/scope.json`, `work/dbnames/todo/` (English DB names, from lang_db.dat / server_db.dat). The
translators' batches (`work/todo`, `work/done`, `work/edit`, `work/dbnames/done`) are local work files too;
`python tools/merge.py` (units) and `python tools/merge.py --dbnames` fold them into `translation/he/`.
Fresh checkout: `extract.py`, `dbnames_scope.py`, then `build.py --ltc` and `coverage.py`.

## Text

- Built-in languages live in `data\game_simulation\languages.fmf`. **fmf** = header + one zstd *seekable*
  stream per file (4096-byte frames + a seek-table skippable frame) + an index frame at the end
  (`tools/fmf.py` reads, extracts and rebuilds it byte-exactly except for the index frame's compression).
- `english.ltc` (compiled language, `tools/ltc.py`, round-trips byte-identically): **198,791 strings,
  ~3.0 million words**, many with FM's token grammar (`[%person#1-he]`, `[%team#1-short]`, `{s}`), plus
  several random variants per id.
- **The supported mod path:** FM writes a template `Documents\Sports Interactive\Football Manager 27\
  languages\example.ltf` (text: `LANGNAME`, `GENDERS`, `BASESTRINGS`, `GENDERINFO`, then
  `KEY-<id>[-M|-F|-A|-B]: English` / `STR-1: translation`, 371,202 entries incl. male/female variants;
  `tools/ltf.py`). A file `hebrew.ltf` there is compiled by FM into `hebrew.ltc` on start and is used when
  `%LOCALAPPDATA%\Sports Interactive\Football Manager 27\Preferences\version 6\current_language.xml` says
  `hebrew`. **Tested 2026-11-25: works** (all UI text switched to our test strings).

## Rendering

Tested 2026-11-25 (test language = "שלום " + English, launched through the proxy):
- **Glyphs: solved.** Replacing the embedded TTF of every Latin font (`LanguageFallback`, `ABCSocial`,
  `ABCSocialCondensed`, `GT-America`, `NotoSans`, `ExtraGlyphs` in `ui-fonts_assets_production.bundle`, and
  `NotInter` in `ui-styles_assets_common/default.bundle`) with Noto Sans + Noto Sans Hebrew (UnityPy) makes
  Hebrew render; the proxy redirects UnityPlayer's opens of those three bundles to our copies
  (`pack/redirect.cfg`). Hooking UnityPlayer.dll is fine; the anti-tamper only reacts to game_plugin hooks.
- **Letter order inside Hebrew runs: correct** (Unity bidi). **Paragraph direction: LTR** (mixed
  Hebrew/Latin lines will be ordered left-to-right, text left-aligned). Next: try wrapping strings in RLE/PDF
  or RLI/PDI; otherwise accept left alignment.

### Earlier notes

- **Glyphs:** UI fonts are TextCore dynamic font assets in
  `fm_Data\StreamingAssets\aa\StandaloneWindows64\ui-fonts_assets_production.bundle`; none has Hebrew
  (test showed boxes). The main font `ABCSocial-Regular SDF` falls back through 6 assets, one is
  `LanguageFallback` (dynamic). Plan: replace `LanguageFallback`'s embedded TTF with Noto Sans + Noto Sans
  Hebrew (OFL) via UnityPy, as a bsdiff'd copy of the bundle loaded only in Hebrew sessions.
- **Right-to-left:** the test text was laid out left-to-right (no bidi). The Unity layer has RTL code
  (`IsRightToLeftLayout`, `MirrorForRTL`, `ForceRightToLeft`, `IsHebrewCharacter`), apparently switched on for
  Arabic. To check: what turns it on (language id/name?), else pre-reverse strings (visual order) in the ltf.

## Launch-only design

- `game_plugin.dll` must not be touched: with IAT hooks in it the game quit right after loading
  translation data (anti-tamper). Hooks in `UnityPlayer.dll`/`fm.exe` only.
- Proxy `version.dll` next to `fm.exe` (UnityPlayer imports VERSION.dll; source `tools/proxy`, export list
  `exports/version.txt`). With `-tirgumim_he`: put `hebrew.ltf` into the user languages folder and set
  `current_language.xml` to `hebrew` (original kept, restored at exit; and on any later start without the
  flag, so a Steam launch is English even after a crash); redirect the fonts bundle (UnityPlayer's CreateFileW).

## In-game proof (2026-11-25, Steam launch with `-tirgumim_he`)

Proxy `version.dll` + `tirgumim\he\` (pack/redirect.cfg): it swaps `current_language.xml` to `hebrew`
(pack/current_language.xml), places `hebrew.ltf` in the user languages folder, redirects the three font
bundles, and holds a named mutex so other programs loading the DLL (Unity's crash handler) don't clean up
under the running session. Result: main-menu sample strings in Hebrew with Hebrew glyphs. After the game
was killed, the preference was back to `english` and `hebrew.ltf`/`hebrew.ltc` were gone. A normal Steam
launch with the proxy installed was English, and saves and preferences were unchanged.
- **Mixed Hebrew/Latin lines:** wrap every string in RLI…PDI (U+2067…U+2069). Word order is then right
  and nothing visible is drawn. Plain strings and an RLM prefix get it wrong, and RLE draws a small mark.
- **Text is left-aligned.** Fine for now; FM's Unity RTL layout (Arabic) isn't switched on for custom languages.

## In-game token test 2026-11-26

`tools/gender_test.py` writes a full test `hebrew.ltf` in which every entry is a marker + its English
(`^` key without variants, `0~` base key of a gendered family, `M~`/`F~`/`MF~`/`A~`... the variant), and
summarises the `hebrew.ltc` FM compiles from it. Launched through the proxy with `-tirgumim_he` (no font
maps: the markers are ASCII), quick-start career at Angel City FC (NWSL), up to the "Breaking News" screen
(no career begun, nothing saved). Screenshots in `work/test/` (gitignored): `g0-07`, `g0-09` (male manager),
`r2-35`, `r2-48`, `r2-52` (female manager "d t", She/Her), `g2-06`/`g2-07` (GENDERS 2), `r2-29`, `r2-40`, `r2-53`.

- **Gender variants: the game always prints the base key.** FM compiles each family into one record
  `[base, M, F]` (`[base, MM, MF, FM, FF]`, ...) whatever the header says: the `.ltc` from `GENDERS: 0` and
  from `GENDERS: 2` are byte-identical. In game the male and the female manager both got `0~` texts (news
  item 688794 "...under her leadership", tendencies 701864, playing-career 695810/695799), in both GENDERS
  runs. `-M`/`-F`/`-MF`/`-A`/`-B` texts were never shown, so the variant-only units need no translation.
  The pronoun tokens in the base text (`[%person#1-his]` -> "her") are resolved by the engine in English.
- **Consequence for {m,f} splits:** a base key has one string, so it cannot carry a male and a female
  Hebrew text. There is no tool yet that writes `hebrew.ltf` from `translation/he/units.json`
  (`ltf.write` writes one `STR-1` per key; `merge.py` keeps `{m, f}` objects as they are). Either the base
  text must be gender-neutral, or (untested) the compiled `.ltc` records would have to be rewritten into
  French's form `[M, F]` (French records have no base; FM picks by gender there), which the proxy would
  then have to place instead of letting FM compile the ltf.
- **Token sources:** `[%team#1-short]`/club names, `[%stadium#1]`, `[%nation#1-nationality]` ("Israeli",
  "Afghan"), nation names (U.S.A., Israel, Afghanistan in UI lists), competition names in fixtures, people
  names: **native/database English**, not our ltf (the ltf has nation keys such as 248286 "Israel", but they
  were not used). `{s}` printed nothing. The nationality picker in manager creation does use ltf keys
  (`0~Afghan`). Ordinals (`^8th`), job names in the job picker (`^Manager`, plain keys without variants)
  and position abbreviations (`^GK`, `^D^C`) come from our ltf. Not seen in this test: award, stage_name,
  conditions, and a `[%job#N]`/`[%position#N]` token inside a sentence.
- **Feminine job/position nouns:** none available. Job keys ("Manager" 227980..., "Assistant Manager")
  have no `-F` variant, and where position keys do ("Goalkeeper" 688055-F, "Striker" 688067-F) the base is
  what is printed; female players in Best XI showed the plain `^` position keys. Write job/position texts
  so they read for both genders.

## Gendered records and DB names (research 2026-11-26)

Files only (no game run). Tools: `tools/ltc_write.py` (full .ltc reader/writer and our own ltf compiler),
`tools/langdb.py` (per-language DB names), `tools/gender_test.py --male-base`.

### How the engine picks a gender variant

- **.ltc layout** (in the `ltc_write.py` docstring): magic, index pos, **u32 source size**, name, **u32
  trailer**, records `u8 n` + n strings, index `(id, offset | 0x80000000 flag)`, tail. `id = 0x10000000 +
  ltf key`. Shipped files: source size 0, trailer 1001, tail = the GENDERINFO article tables (French
  "de"+"le" -> "du" etc.; `u32 0` for English and Arabic). FM's compile of our ltf: source size = **size in
  bytes of the .ltf** (227,342,498 = `hebrew_g0.ltf`), trailer 0, tail `u32 0`, no flags, no 0x2..0x6 ids.
- **No header field or per-record flag says "pick by gender".** French, German, Spanish, Russian, Polish,
  Greek, Italian and Arabic all have the same header as English; the index flags (about 1,000 entries,
  same in every language including English) are not about gender, and GENDERS/GENDERINFO only feed the
  article tail. The only difference is the records: French `[M, F]`, `[MM, MF, FM, FF]`, but also 3, 5, 6,
  7-variant records in no fixed order (e.g. 268780 is F/M, F/F, M/M). Every variant carries its genders
  as tokens: `[%male#1]`, `[%female#2-surname]`, and where the text shows none, `-hidden` ones
  (`...la mi-temps[%male#3-hidden][%female#1-hidden]`, `Gardien de but[%male#1-hidden]`). So **the engine
  picks the variant whose `[%male#N]`/`[%female#N]` tokens fit the people passed in.** Our compiled
  records are `[base, M, F]` and the base has `[%person#1]`, which fits everybody, so the base always won;
  that is exactly what the 2026-11-26 test showed. (French also has ~5,900 two-variant records with no
  gender tokens at all, e.g. 613335 "Désolé..." / "Désolée..."; how those are picked is not visible in the
  files: probably by position, M first.)
- **Our compiler = FM's compiler:** `ltc_write.py compile work/test/hebrew_g0.ltf` (and `_g2`) gives a file
  byte-identical to the `hebrew.ltc` FM wrote. Rules found on the way (the future `build.py` must follow
  them): an STR is **one line** (FM drops continuation lines, so write `\n`); `[...]` that is not a `[%`
  token is removed (`DoB[Comment - Date of Birth]`); `\"` `\'` `\\` are unescaped; the string is trimmed;
  a key whose English is empty after that is dropped (648473 `[+%fraction#1-.0]`). Every shipped .ltc
  (English, French, German, Greek, Arabic) and FM's own compile round-trip byte-identically.

### Two ways to get male/female Hebrew

- **A. ltf only (no new mechanism):** write the base key's STR-1 as the male text with `[%male#N]` tokens
  (adding `[%male#N-hidden]` if the text has none), `-M` the same, `-F` the female text with `[%female#N]`.
  The compiled record `[male, male, female]` then gives a woman the `-F` text if the engine skips variants
  whose tokens don't fit. All 30,868 split base keys have template variants (families of 3/5/9/17/33), so
  this covers every split; units.json splits already use `[%male#1]`/`[%female#1]` (only 2 of 30,721 have
  no gender token; the writer adds a `-hidden` one).
- **B. our own .ltc in French form:** `python tools/ltc_write.py hebrew <out> [--ltf <ltf>]` writes split
  units as `[m, f]` (no base) and everything else as one record with the base text (RLI...PDI around
  Hebrew), sorted like FM's compile. `work/test/hebrew.ltc` (34.7 MB, 197,993 records: 30,868 split,
  156,584 plain, 10,541 English) is the candidate from the current units.json. The proxy would place it
  with `place=` like the ltf. Whether FM then recompiles is not in the files: the header's source-size
  field is the only staleness data FM writes (no hash, no timestamp), so the candidate gets the size of the
  ltf placed with it, and the proxy copies files in cfg order with their timestamps (std::fs::copy keeps
  them), so the .ltc stays newer than the .ltf.

### In-game test (about 5 minutes, next away window)

Ready in `work/test/pack-ltc/` (gitignored): `hebrew.ltf` = `gender_test.py --male-base` markers (`0~` base
= the English **male** variant, `M~`/`F~`/`MF~`... variants, `^` plain), `hebrew.ltc` = `ltc_write.py hebrew
--markers --ltf` (`L^` plain, `LM~`/`LF~` French-form records, untranslated families as their English
variants `LM~`/`LF~`/`LMF~`...), header source size = that ltf's size, `redirect.cfg` (places both, no font
maps: markers are ASCII, Hebrew may show boxes), `redirect-ltc-only.cfg`.
1. Copy `work/proxy-target/release/tirgumim_proxy.dll` to the game folder as `version.dll` and the
   contents of `work/test/pack-ltc/` to `<game>\tirgumim\he\`. Start from Steam with `-tirgumim_he`.
2. Main menu: does text start with `L` (`L^`)? **Yes = FM used our .ltc** (no recompile). Plain `^` = FM
   recompiled from the ltf.
3. Quick-start career, male manager, Angel City FC (as before), to the "Breaking News" screen: read the
   new-manager news (key 688794, "A new dawn..."), the manager profile tendencies (701864 "Plays Attacking
   Football") and playing career (695810 / 695799). Note the marker of each.
4. Back out without starting (Escape, no Enter on menus), new quick start with a **female** manager
   (She/Her), same screens, same keys.
5. Quit. Check that `Documents\...\languages\hebrew.ltf`/`.ltc` are gone and the language is `english`.

Reading the result:
| seen (male / female) | meaning | path |
|---|---|---|
| `LM~` / `LF~` | our .ltc is loaded and French form works | B |
| `L...` / `LM~` for the woman | .ltc loaded, but the engine does not pick by tokens | neither; neutral Hebrew |
| `0~` / `F~` | FM recompiled the ltf; picking by tokens works | **A** (simplest: no .ltc at all) |
| `0~` / `0~` | recompiled, and the first variant always wins | try B with `redirect-ltc-only.cfg` |

If FM recompiled (no `L`) and time is left: rename `redirect-ltc-only.cfg` to `redirect.cfg` (only the
.ltc is placed) and repeat steps 2-4 once: `L` texts mean the .ltc alone is loaded.

### English database names

What the in-game test saw as "native/database English" (club, stadium, competition, nation names,
nationality adjectives) are database fields, not language strings:
- **Per-language name sets ship with the database:** `shared\data\database\db\2700\2700_fm\lang_db.dat`
  (an fmf inside a `dat.` wrapper) holds `<language id>_<table>.dat` for 25 language ids (8 English, 10
  French, 11 German, 12 Greek, 2 Arabic, 1000002 Chinese...; list in `tools/langdb.py`). **No Hebrew id.**
  Gendered languages carry the grammatical gender of each name and several nationality forms (French
  algérien / algérienne / algériens / algériennes). The native code loads them as
  `set_data_lang_names_clubs/nations/comps/stadiums/...` for `current_db_language`. A custom ltf language
  showed English names, so it gets the English set (8).
- **.lnc name-change files** (UTF-16 or UTF-8 text, tab separated): `"CLUB_LONG_NAME_CHANGE" <id> "name"
  <language>`, also `CLUB_SHORT_`, `NATION_LONG_/SHORT_NAME_CHANGE`, `NATIONALITY_NAME_CHANGE`,
  `COMP_LONG_/SHORT_NAME_CHANGE`, `STADIUM_NAME_CHANGE`, `STAGE_NAME_*`, `AWARD_LONG_NAME_CHANGE`,
  `*_GENDER_CHANGE`. The language column is a numeric id (8, 1000002) or a name (`"Greek"`); no column =
  all languages. Read from `shared\data\database\db\<version>\lnc\all\`, `lnc\<language>\` (`greek\`), and
  `lnc\platform\`; the native code also has an `additional_lnc_folder` setting (not set anywhere in the
  install; where it is read from is unknown). `.dbc`/`.edt`/`.ddt` (same folders, `dbc\`, `edt\`) are data
  edits, not names. `Documents\...\editor data\` is empty here (only a config.xml with `dont_scan`).
- **Answer:** there is no ready per-language slot for a language FM doesn't know. Options, best first:
  1. (Chosen, as a redirect instead of a swap: see "Hebrew database names" below.) Session-only copy of
     `lang_db.dat` whose English tables (`8_*`) carry Hebrew names, swapped in by the proxy (`swap=` with an absolute game path; the proxy needs a `{Game}` tag) and put back at exit.
     Hebrew sessions only, no hook. To check: that names are re-read from lang_db when a save loads (the per-language
     `set_data_lang_names_*` loaders suggest they are not baked into saves) and that
     `fmf.rebuild` can be pointed at the inner fmf of the `dat.` wrapper.
  2. `.lnc` with language `"Hebrew"` placed by the proxy into `lnc\all\` for the session: only if the
     language column matches a custom language's name (untested), and lnc changes may be applied at new
     game and stored in the save (then an English session of that save would show Hebrew).
  3. A native hook: no (game_plugin.dll must not be touched).
- **Size** (English set): 251 nations (long + short names, 249 distinct nationality adjectives, which in
  Hebrew need m/f/pl forms), 8,084 competitions (a few hundred are top leagues, cups and continental;
  the rest lower and youth divisions), 100,432 club records (reserves, youth and women's teams included;
  playable top divisions are a few thousand), 52,406 stadiums, 58,475 cities, 3,902 awards, 2,532 + 1,681
  regions, 924 derbies, 288 stage names. Realistic first set: nations + nationalities + continental and top
  competitions (~1,000 strings), then clubs of the main leagues.

## Hebrew database names (decided and built 2026-11-26, files only)

**Decision: no in-place swap.** The Hebrew names reach the game only through the proxy's file redirect:
with `-tirgumim_he`, the game's open of `shared\data\database\db\2700\2700_fm\lang_db.dat` opens
`tirgumim\he\lang_db_he.dat` instead (`map=` in `pack/redirect.cfg`). The original file is never written,
so a crash can never leave Hebrew for a Steam launch. If an `.lnc` fallback is ever needed, it is
redirected the same way (`add=` makes a file appear in `lnc\all\` for the session only).
- **The redirect needs kernel32 in `modules=`.** lang_db.dat is opened by `game_plugin.dll` (its imports:
  KERNEL32 CreateFileW, CRT fopen), whose import table we must not touch. kernel32's `CreateFileW`,
  `GetFileAttributes*`, `FindFirstFile*`... are `jmp [IAT]` stubs into kernelbase (checked in this PC's
  System32), so the proxy now also patches **kernel32's** own import table (and ucrtbase's, for fopen): every
  module's file calls pass our lookup without any byte of game_plugin changing. The hooks call the kernelbase
  functions directly (no re-entry); LoadLibrary is not hooked in system modules. Whether the anti-tamper
  also checks kernel32's import table is unknown: first thing the in-game test shows.
- `{Game}` tag: not needed (`map=` paths are game-relative already).
- The database folder name (`2700`, `2700_fm`) changes with FM's database updates: check the path after
  every game update (an official data update would also change record counts; rerun the scope script).

**Definition of complete for FM27 DB names** (Hebrew in the English `8_*` tables; everything else stays as
in the database):
- **Nations:** all 251 (long + short) and their nationality adjective. Translators give m / f / m pl / f pl;
  the English table has one form, so the game gets the masculine singular (it prints it for women too, like
  the English).
- **Competitions:** every competition of a playable nation and every continental / international one.
  Priority A (1,370 items, 23 batches): top two divisions, cups / super cups / play-offs / stages (level
  100), continental and international senior comps. Priority B (`competitions_lower`, 4,566 items, 58 batches):
  lower and regional divisions, youth, reserve, women's lower leagues. Both are in scope; A ships first.
- **Clubs, their stadiums and cities:** every club in the top two divisions of the playable nations
  (men's 51 nations, women's 15), plus every Israeli club. Transliteration as Israeli sports media write
  names (`work/dbnames/TRANSLATOR.md`, `glossary.md`).
- **Awards:** all 3,902 records (3,869 distinct long/short pairs).
- Out of scope (English as in the DB): lower-tier and unplayable-nation clubs, their stadiums and cities;
  three/four-letter codes; regions, derbies, stage names, media, injuries (injuries come from the ltf).

**Which records (decoded from server_db.dat, `tools/dbnames_scope.py`):** server tables are in the same
record order as the lang tables, records end with `u32 row, u32 id, u32 id`, and records point at each
other by row. Clubs: u32 @13 nation row, @17 city row. Teams (`table_24`, clubs + national teams): u16 @3
reputation, u32 @5 current division (comp row), @9 last division, @17 stadium row. Comps: u16 @16 level (0 =
top, 1 = second, 100 = cup/other), nation row after the season years. Women's clubs have ids from
2,000,000,000. All 100,432 club, 100,930 team and 8,084 comp records split cleanly. **Gap:** "playable by
default" is not a field we found; `PLAYABLE` / `WOMEN_PLAYABLE` in the script are the FM26/27 playable
league nations (edit and rerun). 86 comps have no nation (Friendly, Club World Cup, B internationals...):
taken as international.

**Counts (2026-11-26):** 146 top-two divisions (112 men's, 34 women's; split second tiers such as Argentina
A/B, Australian NPL states, USL East/West, Cymru North/South are all included). In scope: 251 nations, 251
nationalities, 5,936 competitions (1,370 A + 4,566 B), 2,851 club records (2,756 distinct names), 1,982
stadiums, 1,553 cities, 3,902 awards.

**Tools:**
- `python tools/dbnames_scope.py` -> `work/dbnames/scope.json` and the Sonnet batches
  `work/dbnames/todo/<category>-NNN.json` (one item per line; items with the same English share one entry
  with all `ids`), from the player's own lang_db.dat / server_db.dat (gitignored, regenerated). Translators
  write `work/dbnames/done/<same name>.json` with a `he` object per item (gitignored);
  `python tools/merge.py --dbnames` folds them into the tracked `translation/he/dbnames/<category>.json`
  (`{"<db id>": {field: Hebrew}}`, no English).
- `python tools/langdb_write.py` -> `work/dbnames/build/lang_db_he.dat` from `translation/he/dbnames` and the
  game's own lang_db.dat (the English of every field we leave alone comes from there; field length limits
  checked; out-of-range values keep the English). `--check`: all 145 UTF-8 name tables parse and re-join
  byte-identically (Greek 12 has its own layout and is never written) and `fmf.rebuild` of the untouched
  archive is byte-identical to the shipped file (it now handles the 12-byte `dat.` wrapper and keeps the
  original index frame when nothing changed). `--markers`: test copy with `~` + English in every scoped field.
- `tools/langdb.py`: record schemas of the six name tables (`parse_table` / `join_table`).

### In-game test (next away window, about 10 minutes)

Ready in `work/test/pack-dbnames/` (gitignored): `version.dll` (proxy built 2026-11-26 with the kernel32
hooks), `lang_db_he.dat` (`langdb_write.py --markers`: `~Arsenal`, `~Premier League`, `~Emirates Stadium`,
`~London`, `~Israeli`, `~Ballon d'Or`...; ASCII, so no font bundles needed), `redirect.cfg` (only `modules=`
and the lang_db `map=`; no ltf, no preference swap: the UI stays English).
1. Back up `Documents\Sports Interactive\Football Manager 27\games` and the Preferences folder. Copy
   `version.dll` next to `fm.exe` and the other two files to `<game>\tirgumim\he\`. Start from Steam with
   launch options `-tirgumim_he -tirgumim_debug`.
2. If the game quits during loading: the anti-tamper rejects kernel32 hooks. Remove `kernel32.dll` from
   `modules=` and retry once (ucrtbase only); if it still quits, stop and report.
3. Main menu (no career): `%TEMP%\tirgumim_proxy.log` should have `open "...lang_db.dat" redirected`.
4. New career, **quick start**, any club in a top division (as before: Angel City FC, or Arsenal). Only
   Escape and mouse, never Enter on menus (Enter once loaded a save). Look at: the club list in the picker
   (`~` names), the league name, nation flags/names, a player's nationality, the stadium on the club
   overview, the city. A club of a lower division must show its plain English name.
5. Back out without saving (Escape), quit the game. Do not load any save and do not save the new career.
6. Start again from Steam **without** the flag: the same club picker must be plain English (proxy inert).
7. Saves: load nothing, save nothing. What this test can show: names read at a new game come from the
   redirected file. Whether a save keeps them (the `set_data_lang_names_*` loaders suggest names are re-read
   per language, not stored) needs a throwaway saved career, which is a separate decision for the lead:
   started with the flag, saved, then loaded without the flag; `~` names = baked in.
8. Remove `version.dll` and `tirgumim\` from the game folder afterwards; compare
   `%LOCALAPPDATA%\Sports Interactive\Football Manager 27\Caches` with before (only `dbcs\...\ota_1.dbc`
   is there now) to see whether FM cached any names.

## Build (2026-11-26)

    python tools/build.py [--ltc] [--rtl rli|rli-whole|rle|rlm|none] [--no-fonts] [--no-langdb]
    python tools/coverage.py [--list]          the 100% check (exit 0 only when everything passes)

`build.py` (about 40 s; 20 s with `--no-fonts --no-langdb`) reads `translation/he/units.json`,
`work/en/` (from the template `example.ltf`), the game's font bundles and lang_db.dat,
`translation/he/dbnames/`, and writes:
- `work/pack/files/` (the launcher's `filesDir`, our own files): `version.dll` (= `work/proxy-target/release/
  tirgumim_proxy.dll`, built 2026-11-26 with the kernel32 hooks; this PC can't rebuild it, no MSVC) and
  `tirgumim/he/`: `redirect.cfg` (= `pack/redirect.cfg`, option A), `current_language.xml`, `hebrew.ltf`;
  with `--ltc` also `hebrew.ltc`, `redirect-b.cfg` (ltf + ltc placed, ltc after the ltf) and
  `redirect-b-ltc-only.cfg`.
- `work/build/`: the changed copies of game files that `pack/pack.config.json` turns into bsdiff patches with
  `output` into `tirgumim/he/`: the three `*_he.bundle` font bundles and `lang_db_he.dat` (`langdb_write.py`).
- `work/pack/game/`: everything as it goes into the game folder (hard links): copy its contents next to `fm.exe`.
- `work/pack/report.json`: the numbers, and every key left in English with the reason.

**hebrew.ltf (option A)** follows the plan above: base STR of a split unit = m text (with `[%male#N]`, a
`-hidden` one added when missing), each variant gets m or f by the gender its own English gives the split
person (`-MF` -> person 1's letter, etc.; `-A/-B` letters are `male_/female_team/club`), so the compiled record
is `[m, m, f]` / `[m, m, m, f, f]`... Plain units: variants get their own unit's Hebrew, else the base Hebrew
when the English is the same up to gender tokens, else stay English. FM's compile rules are applied (one-line STR,
non-token `[...]` removed, escapes, trimmed, empty-English family dropped); `coverage.py` compiles the built ltf
with our FM-identical compiler and checks every record against the plan. RTL: default `rli` = RLI...PDI around
every *line* with Hebrew (UAX #9 ends an isolate at a paragraph break); `rli-whole` = around the whole string,
exactly what the 2026-11-25 test showed working. `GENDERS: 0` (no effect on FM's compile, research above).
**hebrew.ltc (option B)**: `[m, f]` for split units, `[text]` otherwise, source size = this ltf's size, mtime
set 60 s after the ltf's. FM's own compile of this ltf would be 90,867,129 bytes; our ltc is 35,441,966 bytes.

Numbers on 2026-11-26: 561,574 template keys, 1 dropped (648473, empty English), 560,698 with Hebrew, 875 left
English (variants of one-text units whose English differs from the base beyond gender: typos, "you" pronouns
turned into words; never printed, since the base `[%person#1]` text fits everyone). 197,993 families: 165,550
one-text, 32,443 split (21 split units name two people; the first one decides). DB names: all categories done
except 4 awards (GOAL50, NXGN and their women's versions: short/long left out) and 1 lower comp short name.
Sizes: hebrew.ltf 243 MB, hebrew.ltc 35 MB, lang_db_he.dat 92 MB, fonts 19.2 + 0.5 + 1.3 MB, version.dll 0.2 MB.

**Open gaps:**
- The font builder of 2026-11-25 was never committed; `build.py` rebuilt it (UnityPy, the seven Font slots
  listed under Rendering get Noto Sans + Noto Sans Hebrew, static: Black 900, Condensed width 75, others 400;
  bundles saved LZ4). Not yet seen in game.
- `hebrew.ltf` carries the template's English KEY text (243 MB of the game's text): fine for testing, but the
  published pack should not ship it. Untested ideas: a stub KEY text (FM only needs it non-empty when STR is
  set), or building the ltf on the player's PC from their own example.ltf.
- `pack/pack.config.json`'s lang_db path has the database version (`2700`); check after every game update.

### Away-window test: A or B (and RTL)

1. `python tools/build.py --ltc` (default rtl `rli`). Copy the contents of `work/pack/game/` into the game
   folder (`version.dll` next to `fm.exe`, `tirgumim\he\`). Back up `Documents\Sports Interactive\Football
   Manager 27\games` and the Preferences folder. Start from Steam with `-tirgumim_he` (`-tirgumim_debug` for
   the proxy log).
2. **A** (as copied: `redirect.cfg` places only the ltf, FM compiles it). While the game runs,
   `Documents\...\languages\hebrew.ltc` should be about 90.9 MB (FM's compile). Male manager, then female
   (She/Her), same screens as the token test (news 688794, tendencies 701864, playing career 695810/695799):
   feminine Hebrew for her = A works.
3. **B:** quit, in `<game>\tirgumim\he\` rename `redirect.cfg` to `redirect-a.cfg` and `redirect-b.cfg` to
   `redirect.cfg`, start again. `hebrew.ltc` in Documents still 35,441,966 bytes while running = FM used ours
   (no recompile); then the same male/female screens. If FM recompiled (about 90.9 MB), try
   `redirect-b-ltc-only.cfg` as `redirect.cfg` once.
4. RTL: if mixed Hebrew/English lines or multi-paragraph news read in the wrong order, rebuild with
   `--rtl rli-whole` (or `rle`, `rlm`) using `--no-fonts --no-langdb`, copy `hebrew.ltf`/`hebrew.ltc` again.
5. Quit; the language is `english` again and `hebrew.ltf`/`.ltc` are gone from Documents. Remove `version.dll`
   and `tirgumim\` from the game folder.

## Status

PARKED (decision of 2026-11-25): pipeline proven in game; come back after the other games.
Done: text translated (units.json), DB names, `tools/build.py` + `tools/coverage.py`. To do: in-game test
of the full build (fonts, A/B, RTL), the open gaps above, review pass, launcher test, publish at 100% only.

## Shipping rule and away-window order for the language file (decision 2026-11-26)

The release must never carry the game's English text (GAMES.md rule 4), so `hebrew.ltf` with the template's
English KEY lines is for local testing only. Away-window test order:
1. **(b) ltc only**: ship our `hebrew.ltc` (Hebrew only, [M,F] records) placed by the proxy, no ltf. Pass = FM loads
   the 35.4 MB file (not a ~90.9 MB recompile) and male/female managers see the right forms.
2. **(a) stubbed KEY**: an ltf whose KEY lines carry no English (stub text), Hebrew STR only. Pass = FM compiles it and
   shows the Hebrew.
Ship whichever works; if both do, ship (b) (smaller, no compile). If both fail: a bsdiff patch from the player's own
`example.ltf` (pack `patches/` path, if it supports a different output name - see launcher/DESIGN.md), and only
after that (c) building the ltf in the proxy at session start.
