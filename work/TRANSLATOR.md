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

## Press conferences (from the press-000 review)
- In a split about a player or other person, mark only that person male/female. The manager's dropped "I/my/you" stays
  `[%person#1-hidden]` in both variants (never `[%male#1-hidden]` / `[%female#1-hidden]`).
- "That game" vs "this game" before a match: the previous match is "המשחק הקודם", the coming one "המשחק הזה".
- English metaphors (turn around, dip toes, run X close, uphill) get the Hebrew idiom or the plain meaning; check the idiom table first.
- Keep who is the subject: "I am right for the job" is "אני האדם הנכון לתפקיד", not "the job suits me".
- Every Hebrew clause needs its subject; "the individual" (a player) is "ברמה האישית" / "השחקן עצמו", not "האדם".

## Press conferences (from the press wave-1 review)
- Headlines: no stilted verbal nouns (שקילת, תוכנית ל-). Use "X: <noun> על הפרק", a short quote (מכוונים ל-), or a question.
- Check the gender of every noun a verb agrees with (השפעה, דאגה are feminine: הייתה).
- "X is right" about an unsplit person: "הצדק עם X". No masculine plural noun that covers the manager (כמאמנים): rephrase ("מצדנו").
- "my opinion of X" = "הדעה שלי על X"; "לדעתי" only for "in my opinion". "I prefer" = "אעדיף".
- English present progressive with future meaning ("we're not qualifying") = Hebrew future ("לא נעפיל").
- "hopefully" = "נקווה ש"; "out there" = "על המגרש". Date tokens: "ב-[%date#N-day]", never "ביום [%date#N-day]".

## Scripts
- Keep every script in your OWN subfolder of the scratchpad (e.g. scratchpad\fm-<batch>\), never in the scratchpad root: other batches run at the same time and overwrite shared file names.

## From the press wave-2 review
- Never drop a name token: in a split write it as [%male#N-first]/[%female#N-first]; if you replace it with a pronoun add the -hidden marker. Check the m and f variants separately.
- Pronouns after a preposition: בלעדיו/בלעדיה, עליו/עליה, איתו/איתה, עבורו/עבורה (never "בלי אותו", "עבור אותו"). Never ב- before an infinitive.
- Headlines: no "we" verbs for the manager's own act (מוקירים); "PLAYER: <phrase>" reads as the player's quote, so for news about a player write "X בדרך ל-...".
- A player talking to the manager uses the singular 2nd-person past (הפעלת, אמרת), which reads for both genders.
- In long questions put the main clause first and never put a pronoun before the name it refers to.

## From the rest wave-1 review
- Headlines (X believes / is confident / denies / is satisfied / defends / admits / will stay): never "X: <abstract verbal noun>" (ביטחון ב-, שביעות רצון מ-, הכחשה:, הגנה על, הישארות, הודאה ב-). Use the claim as a short quote ("X: נעלה ליגה", "X: הציפיות לא יעלו"), a same-spelling form ("X: מרוצה...", "X מודה: ..."), the club as subject ("ממשיכים עם X", "האלופה שומרת על X") or "X להגנת Y". Name token first, one colon only.
- No "הודחה / הובסה על ידי X": make the team the subject ("X הדיחה את", "הפסידה ל-X").
- Report openers "It sees / has seen X do Y": "בעקבות זאת / בעקבותיו", never "הוא משאיר" or "גרם ל-X לעבור".
- Watch look-alike verbs: לאכזב (disappoint others) vs להתאכזב (be disappointed). Ask what the sentence means, not what its words are ("separate two sides" = להכריע; "wrong end of the table" = בתחתית).
- Player-development headlines: make the attempt the subject ("הניסיון של X ל-... נכשל").

## From the rest wave-2 review
- Check each Hebrew idiom for false friends ("יצא מגדרו" = go out of one's way, not "be furious").
- Only the manager is addressed in the plural. When anyone speaks to a coach, player or agent, drop the 2nd-person pronoun or use a same-spelling form (שלך, אותך), never "לכם/אתם".
- Duration: "for a while" (stay) = "לאורך זמן"; "זמן מה" means a short time. "recent X" = "X לאחרונה", never "X האחרון".
- Put time/manner phrases ("ahead of schedule") next to the verb they modify.
- For an unsplit person prefer a same-spelling predicate ("X לא מרוצה", "X גאה") over "אצל X יש ...".
- Two conditions joined by "and if" keep the connector: "ובתנאי ש".

## Arguments
- Never write a token (visible or -hidden) for an argument the English text does not have: the game passes only the English arguments. If the English names "the team" or "his manager" in plain words, write plain Hebrew words (הקבוצה, המאמן), not a new [%team#1] or [%job#1].

## Job and position nouns (in-game test 2026-11-26)

FM prints only the base key's text, for men and women alike; no -F variant of a job or position is ever shown. Job titles, position names and role names must therefore read correctly for both genders:
- In labels and lists use the noun as a title (מאמן ראשי, עוזר מאמן, שוער, חלוץ). These read as titles, not as describing a gendered person.
- In sentences about a person, avoid gender agreement with the job: write "בתפקיד [%job#1]" / "בעמדת [%position#1]" rather than an adjective or verb that agrees with the noun.
- Never add a feminine form (מאמנת, שוערת) in a base key text.

## From the rest-062..086 spot check
- Manager Persona news (unsplit [%person#1] hired as manager): never "כמאמן החדש", "למאמן החדש", "המאמן מ-X צפוי", "כניסת המאמן החדש X". Write "מינוי [%person#1] לתפקיד המאמן", "המינוי צפוי להביא", or "[%person#1-surname] מזוהה עם ...". A feminine noun as a stand-in (הדמות, ההדרכה) must not pull a feminine-only predicate (כמנהיגה, כמומחית, כפרגמטית).
- "is set to be confirmed as" = "צפויה לאשר את מינוי X", never "צפוי להיות מאושר". "insiders" = "יודעי דבר", not "גורמים פנימיים".
- Use the UI term inside sentences: Non-EU = "שאינם מהאיחוד האירופי"; GK distribution instructions = "להוציא את הכדור" (labels: הוצאה לאגפים); unhappiness = "חוסר שביעות רצון" (UI: שביעות רצון), never "חוסר אושר".
