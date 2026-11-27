# Instructions for a Football Manager 27 translation batch

You translate **Football Manager 27** (Sports Interactive) into Hebrew for a personal fan translation.

1. Read `D:\AIStuff\Tirgumim\games\football-manager-27\glossary.md` and follow it strictly (token grammar,
   gender rules, football terms, neutral address of the manager).
2. Input `D:\AIStuff\Tirgumim\games\football-manager-27\work\todo\<batch>.json` = `[{"u", "en", "comment"}]`.
   `comment` is the developer's note (screen, context, CHARLIMIT, who is talking): use it, never translate it.
   Units are grouped by game area; neighbouring units are related menu items.
3. Output `D:\AIStuff\Tirgumim\games\football-manager-27\work\done\<batch>.json` = `{"<u>": "<Hebrew>"}` for
   every unit, written with a Python script (UTF-8, ensure_ascii=False) kept in your own folder
   `C:\Users\lidar\AppData\Local\Temp\claude\d3d5937d30b10544\e6f10044-237b-4627-b086-1d7f88c57ca8\scratchpad\fm-<batch>\`.
   If a unit's input has `"gender": "split"`, output an object `{"m": "...", "f": "..."}` instead (male and
   female variants, as glossary.md says).
4. Keep every `[%...]` token argument (variants may change as glossary.md allows), `%s`/`%d`, line breaks and
   `<...>` tags. Respect CHARLIMIT when the comment gives one (Hebrew of similar or shorter length).
5. Check with a script that every unit is present, every `[%type#N` argument of the English appears in the
   Hebrew (except dropped English-only helpers), no `{s}`/`{an}`/`-he]`-style English pronoun variants remain,
   and every output has Hebrew letters (except pure numbers/codes/names). Fix any problem.
6. After each chunk, re-read your Hebrew against the English once for meaning (numbers, negations, objects),
   naturalness (no calques) and the glossary's "Lessons" section, and fix what you find before saving.
7. Work in chunks of a few hundred units and save the output file after each chunk. If the output file
   already exists when you start, keep its entries and translate only the units that are missing.
8. Reply with only: batch done, unit count, new recurring terms decided.
