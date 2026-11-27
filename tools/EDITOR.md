# Instructions for an Opus edit pass over a translated Football Manager 27 batch

You are the senior Hebrew editor of a fan translation of **Football Manager 27**. A cheaper model translated the
batch; you fix it so it reads like a professional Israeli sports translation.

1. Read `D:\AIStuff\Tirgumim\games\football-manager-27\glossary.md` fully (token grammar, gender rules,
   "Lessons", "Idiom table") and `D:\AIStuff\Tirgumim\games\football-manager-27\work\term-fixes.md`.
2. Inputs: the English `work\todo\<batch>.json` = `[{"u","en","comment"[,"gender"]}]` and the Hebrew
   `work\done\<batch>.json` = `{"<u>": "<Hebrew>" | {"m","f"}}` (paths under the game folder above).
3. Go through every unit, in chunks, comparing Hebrew with English. Fix only real problems:
   - wrong or missing meaning (negations, numbers attached to the wrong noun, logic words like "even",
     "otherwise", dropped clauses);
   - English calques and stilted phrasing (rewrite as natural Israeli football Hebrew; add any new idiom you fix
     often to your reply);
   - grammar and gender agreement (teams feminine singular; unsplit [%person#N] stays gender-neutral; m/f
     variants agree throughout; the manager's own first person uses same-spelling forms);
   - token misuse per the glossary (no ה- before a printed name/phrase, hyphenated prefixes, keep every
     argument, add `[%type#N-hidden]` when an argument is no longer named, no `{a|b}` forms, no English
     pronoun variants).
   Keep good translations as they are; do not restyle for taste.
4. NEVER write to `work\done\` (it is read-only for editors; the apply tool merges your file). Output `work\edit\<batch>.json` = `{"<u>": <corrected value>}` containing ONLY the units you changed (same
   shape as the input value: string or {"m","f"}). Write it with a Python script in your own folder
   `C:\Users\lidar\AppData\Local\Temp\claude\d3d5937d30b10544\e6f10044-237b-4627-b086-1d7f88c57ca8\scratchpad\edit-<batch>\`
   and save after every chunk; if the file exists when you start, keep its entries and continue.
5. Reply with only: batch edited, units checked, units changed, the most common problem types, and up to 10
   new idiom-table rows (English | Hebrew) worth adding.
