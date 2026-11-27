# Translator brief: FM27 database names (nations, competitions, clubs, stadiums, cities, awards)

You turn one batch file `work/dbnames/todo/<category>-NNN.json` into `work/dbnames/done/<category>-NNN.json`.
Read `work/dbnames/glossary.md` first and follow it; it wins over anything you remember.

## Input and output

The input is `{"category": ..., "items": [...]}` with one item per line. Each item has `ids` (do not change),
the English fields, and context (`nation`, `division`, `level`, `city`, `women`, `hint_fr`, `hint_fr_forms`...).
The hints are the French/Spanish/German database names. They help you recognise a place or a gendered form.
Do not translate from them.

Write the same file with one key added to every item: `"he": {...}`. Keep every other key unchanged and keep
the items in order. One item per line, UTF-8, valid JSON (escape `"` inside a value as `\"`, e.g. `ת\"א`).

| category | `he` fields | max characters |
|---|---|---|
| nations | `long`, `short` | 32 / 25 |
| nationalities | `m`, `f`, `mpl`, `fpl` (masc. sg., fem. sg., masc. pl., fem. pl.) | 25 each |
| competitions, competitions_lower | `long`, `short` (`abbr` only if a Hebrew one is in real use, otherwise omit) | 50 / 25 / 4 |
| clubs | `long`, `short`, optional `abbr6` (up to 6 letters, for very narrow columns), optional `nickname` | 50 / 25 / 6 / 39 |
| stadiums | `name`, plus `alt_name` when the English has one | 50 / 48 |
| cities | `name` | 40 |
| awards | `long`, `short` | 75 / 50 |

If a field is longer than its limit, the writer keeps the English, so shorten it yourself (drop the sponsor,
use the common short form). Leave a field out, or set it to "", when the English should stay. Three- and
four-letter codes (ARS, MTA, PL) are never translated: they are not in `he`.

## Transliteration (clubs, stadiums, cities, people in award names)

Write names the way Israeli sports media do (ONE, ספורט 5, Walla! Sport, ynet sport). Use the established
Hebrew form when one exists. Spell everything else by how it sounds in the original language, not letter by
letter from English.

- **Geresh** for sounds Hebrew lacks: צ' (ch: צ'לסי, צ'יבס), ג' (j/soft g: ג'נואה, ג'ובנטוס), ז' (zh/French j:
  ז'ירונה only when said that way; Girona is ג'ירונה), ת' only in established forms. Final letters ם ן ץ ף ך at
  word end (ברצלונה, ליון, בורוסיה דורטמונד).
- **Vowels:** ו for o/u, י for i/e where it helps reading (ריאל, ליברפול, אינטר). Do not add a י for every e.
  ע and ח only for names that have them (ח for Spanish j/German ch: חטאפה, מונכנגלדבאך).
- **Common forms** (always these):

| English element | Hebrew | example |
|---|---|---|
| FC / F.C. / CF / SC / AC (prefix or suffix) | dropped | Liverpool FC -> ליברפול, AC Milan -> מילאן |
| FC, AFC as part of a famous name | kept only in the established form | FC Barcelona -> ברצלונה, AFC Bournemouth -> בורנמות' |
| United / Utd | יונייטד | מנצ'סטר יונייטד, ניוקאסל יונייטד |
| City | סיטי | מנצ'סטר סיטי, לסטר סיטי |
| Real | ריאל | ריאל מדריד, ריאל סוסיאדד |
| Athletic / Atlético | אתלטיק / אתלטיקו | אתלטיק בילבאו, אתלטיקו מדריד |
| Sporting | ספורטינג | ספורטינג ליסבון |
| Inter / Internazionale | אינטר | אינטר |
| Milan | מילאן | מילאן |
| Borussia | בורוסיה | בורוסיה דורטמונד |
| Olympique | אולימפיק | אולימפיק מרסיי |
| Dynamo / Dinamo | דינמו | דינמו קייב |
| Rovers / Wanderers / Albion / Hotspur / Rangers / Celtic | רוברס / וונדררס / אלביון / הוטספר / ריינג'רס / סלטיק | טוטנהאם הוטספר (short: טוטנהאם) |
| Club Atlético, Sport Club, Esporte Clube... (Latin American long names) | long: the full name transliterated; short: the name people use | Club Atlético Boca Juniors -> long בוקה ג'וניורס |
| Women / Women's / Ladies team (item `women: true`) | the same name as the men's club; no "נשים" unless the English name itself says Women | Arsenal (women) -> ארסנל |
| B / II / reserve suffix | keep it: ב' or 2 | ריאל מדריד קסטייה, בורוסיה דורטמונד 2 |

- **Israeli clubs** keep their Hebrew names exactly as the clubs write them: מכבי תל אביב, הפועל באר שבע,
  בית"ר ירושלים, מכבי חיפה, בני סכנין, הפועל ירושלים, מ.ס. אשדוד, עירוני קריית שמונה. Short names as the
  media write them (מכבי ת"א, הפועל ב"ש, בית"ר י-ם). Hyphens in the English (Tel-Aviv, Petach-Tikva) are not
  Hebrew: פתח תקווה.
- **Sponsor names** in stadiums and competitions: transliterate them (סטדיון אמירייטס, ספוטיפיי קאמפ נואו).
  If a non-sponsor name is in `alt_name`, translate both.
- Club-form prefixes and founding years go when the media drop them: 1. FC Köln -> קלן, TSG 1899
  Hoffenheim -> הופנהיים. A number that is the name stays: 1860 München -> 1860 מינכן, Schalke 04 -> שאלקה.

## Exonyms (nations, cities)

Use the Hebrew exonym when there is one: גרמניה, ספרד, צרפת, איטליה, אנגליה, סקוטלנד, וויילס, צפון אירלנד,
אירלנד, הולנד, בלגיה, שווייץ, אוסטריה, יוון, טורקיה, רוסיה, אוקראינה, פולין, צ'כיה, ארצות הברית, מקסיקו,
ברזיל, ארגנטינה, יפן, דרום קוריאה, סין. Cities: לונדון, מינכן, רומא, מילאנו (city; the club is מילאן),
טורינו, נאפולי, פירנצה, ונציה, ליסבון, פורטו, מוסקבה, קייב, ורשה, פראג, וינה, ז'נבה, ציריך, קלן, אמסטרדם,
בריסל, אתונה, איסטנבול, בלגרד, בוקרשט, סביליה, ולנסיה, ברצלונה, מדריד, ניו יורק, לוס אנג'לס.
FM's state suffixes stay in Latin as they are: Rosario (SF) -> רוסאריו (SF), Santos (SP) -> סנטוס (SP).

## Nationalities (m / f / plural)

| nation | m | f | mpl | fpl |
|---|---|---|---|---|
| Germany | גרמני | גרמנייה | גרמנים | גרמניות |
| Spain | ספרדי | ספרדייה | ספרדים | ספרדיות |
| Israel | ישראלי | ישראלית | ישראלים | ישראליות |
| England | אנגלי | אנגלייה | אנגלים | אנגליות |
| France | צרפתי | צרפתייה | צרפתים | צרפתיות |
| United States | אמריקאי | אמריקאית | אמריקאים | אמריקאיות |
| Brazil | ברזילאי | ברזילאית | ברזילאים | ברזילאיות |

Rules: -י / -ייה / -ים / -יות for most; -אי / -אית / -אים / -איות where the press uses it (ברזילאי,
אמריקאי, קוריאני is -י). The feminine is -ית for some common adjectives (ישראלית, אמריקאית, קנדית):
use the form the press uses. Historic states: Soviet Union -> סובייטי, Yugoslavia -> יוגוסלבי, West
Germany -> מערב גרמני. If no adjective is in real use (Saint Kitts and Nevis), write "מ" + the country in
all four forms (מסנט קיטס ונוויס). The game prints the masculine singular (`m`) for every player, women
too; the other forms are kept for later.

## Competitions

| English | Hebrew |
|---|---|
| Israeli Premier League / National League / State Cup / League Cup (Toto Cup) / Super Cup | ליגת העל / הליגה הלאומית / גביע המדינה / גביע הטוטו / אלוף האלופים |
| Premier League / Championship / FA Cup / EFL Cup | הפרמייר ליג / הצ'מפיונשיפ / הגביע האנגלי / גביע הליגה האנגלי |
| Spanish First Division (La Liga) / Second / Copa del Rey | לה ליגה / הליגה השנייה בספרד / גביע המלך |
| Italian Serie A / Serie B / Coppa Italia | הסרייה A / הסרייה B / גביע איטליה |
| Bundesliga / 2. Bundesliga / DFB-Pokal | הבונדסליגה / הבונדסליגה 2 / הגביע הגרמני |
| Ligue 1 / Ligue 2 / Coupe de France | הליגה הצרפתית / ליג 2 / הגביע הצרפתי |
| UEFA Champions League / Europa League / Conference League / Super Cup | ליגת האלופות / הליגה האירופית / הקונפרנס ליג / סופר קאפ האירופי |
| World Cup / European Championship / Nations League / Copa América | המונדיאל / היורו / ליגת האומות / קופה אמריקה |
| World Cup qualifying (Europe) | מוקדמות המונדיאל (אירופה) |
| U21 / U19 / Women's | עד גיל 21 / עד גיל 19 / נשים |
| First / Second / Third Division of X | הליגה הראשונה / השנייה / השלישית ב[מדינה] |
| Group A, North/South Division | בית A, מחוז צפון / דרום |
| Cup / League Cup / Super Cup / Play-offs | גביע / גביע הליגה / סופר קאפ / פלייאוף |

Sponsored league names: the established Hebrew name without the sponsor (Sky Bet Championship -> הצ'מפיונשיפ,
Ligue 1 McDonald's -> הליגה הצרפתית). `short` is what a fixtures list shows: up to 25 characters, usually
the same without "ה" at the start when the long name needs it (`long` הפרמייר ליג, `short` פרמייר ליג).

## Awards

Translate the meaning in the style of Israeli sports news: Player of the Year -> שחקן העונה,
Young Player of the Year -> השחקן הצעיר של העונה, Manager of the Month -> מאמן החודש, Team of the Year ->
נבחרת העונה, Golden Boot -> נעל הזהב, Ballon d'Or -> כדור הזהב, Golden Glove -> כפפת הזהב. Keep the
competition name in Hebrew as in the competitions table (שחקן העונה בפרמייר ליג). Named awards keep the
person's name transliterated (גביע מאט באזבי). `short` up to 50 characters.

## Quality

- One name, one Hebrew form: the same club, city or competition must read the same in every batch. Add any
  new recurring form to `work/dbnames/glossary.md` (end of the file, one table row) and use it.
- No English letters in `he` except codes inside a name (A, B, 2, 1860, `(BA)`).
- Never invent a translation for a name you do not recognise: transliterate it by its language.
- Return only the done file. Do not edit todo files, scope.json or the glossary's existing rows.
