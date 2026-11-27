# Glossary and rules: Football Manager 27 (Hebrew)

Football management simulation. Register: modern Israeli football Hebrew, as in sports websites (ONE, ספורט5)
and Israeli club announcements; concise UI; news and press in journalistic Hebrew; player and staff speech
natural and spoken. The human manager ("you") can be male or female: UI that addresses the player is written
gender-neutral (infinitive / noun / plural: "בחירת שחקן", "לחצו"), never masculine-only.

## Token grammar (how Sports Interactive's own French/Arabic translations work; follow it)
Tokens look like `[%type#N-variant]`; N is the argument number (1, 2, author...). Keep every argument's
tokens; you may reorder them, change their variant, or drop pure-English helpers as listed below.

- **People:** `[%person#N]` (gender unknown in English), `[%male#N]`, `[%female#N]`.
  - Name variants you may use: `[%x#N]` full name, `-surname`, `-first`, `-hidden` (prints nothing).
  - **English pronoun variants are dropped:** `-he -she -his -her -him -himself -herself -I -me -my -you
    -your -He -His -You...` print English words. Write the Hebrew pronoun or suffix in the text instead
    (הוא/היא, שלו/שלה, -ו/-ה, אני, אתה/את...). If the sentence then no longer names that argument, add
    `[%male#N-hidden]` (or `[%female#N-hidden]`) at the end so the game still knows the argument.
  - **Gender:** in `-M` keys the person is male, in `-F` keys female: use `[%male#N...]` / `[%female#N...]`
    as the English does and Hebrew forms to match. In keys without a suffix whose English uses
    `[%person#N]` with pronouns, give **two variants** (male, female) as the output says (see TRANSLATOR.md);
    in the male variant replace `[%person#N...]` by `[%male#N...]`, in the female one by `[%female#N...]`,
    and end each variant with the matching `-hidden` markers of every gendered argument (as French does).
- **Teams/competitions:** `[%team#N]`, `-short` (preferred), `-nickname`, `-typeonly`, `[%comp#N]`,
  `-short`, `[%club#N]`, `[%male_team#N-...]` / `[%female_team#N-...]`. Team names stay as the game prints
  them; build Hebrew around them: "שחקני [%team#1-short]", "ב-[%team#1-short]" (prefix letters attach with a
  hyphen to a token: ב-, ל-, מ-, ש-, ה-, ו-).
- **Numbers, money, dates:** `[%number#N]` (digits; prefer it over `-text`/`-nth`, which print English:
  write "מקום [%number#1]", "המשחק ה-[%number#1]"), `[%cash#N...]`, `[%date#N...]`, `[%time#N]`,
  `[%season_year#N]`, `[%scoreline#N...]` keep as they are.
- **Others** (`[%position#N...]`, `[%job#N]`, `[%nation#N...]`, `[%stadium#N]`, `[%injury#N]`,
  `[%string#N]`, `[%media_source#N]`, `[%person_list#N]`...) keep; they print text from other translated
  strings. `-lowercase` is harmless.
- **Brace helpers:** `{s}` (English possessive) and `{an}`/`{An}`/`{a}` (article) are dropped; `{upper}`,
  `{Upper}`, `{lower}` are dropped too (Hebrew has no case). Keep any other `{...}` you don't understand.
- `~1~`-style markers, `%s`, `%d`, `\n`/line breaks, `<...>` tags, `|` and `[COMMENT...]`: COMMENT is the
  developer's note (do not translate, do not output it); keep every other marker exactly.

## Football terms
| English | Hebrew |
|---|---|
| manager / head coach | מנהל / מאמן ראשי (the job titles; in prose "המאמן") |
| assistant manager | עוזר מאמן |
| chairman / board | יו"ר / ההנהלה |
| director of football | מנהל מקצועי |
| scout / scouting | סקאוט / סקאוטינג |
| squad / first team / reserves / U21 / U18 | סגל / קבוצה ראשונה / קבוצת מילואים / עד גיל 21 / עד גיל 18 |
| fixture / match / friendly | משחק / משחק / משחק ידידות |
| league / cup / division / table | ליגה / גביע / ליגה (ליגה שנייה...) / טבלה |
| promotion / relegation | עלייה / ירידה |
| transfer / loan / free transfer / release clause | העברה / השאלה / העברה חופשית / סעיף שחרור |
| contract / wage / signing-on fee / agent | חוזה / שכר / מענק חתימה / סוכן |
| transfer window / deadline day | חלון העברות / יום הסגירה |
| goalkeeper / defender / midfielder / forward / striker / winger / full-back / centre-back | שוער / מגן / קשר / חלוץ / חלוץ / כנף / מגן / בלם |
| formation / tactic / mentality / pressing | מערך / טקטיקה / גישה / לחץ |
| set piece / corner / free kick / penalty / throw-in | מצב נייח / קרן / בעיטה חופשית / פנדל / חוץ |
| clean sheet / hat-trick / assist | שער נקי / שלושער / בישול |
| yellow card / red card / suspension | כרטיס צהוב / כרטיס אדום / הרחקה |
| injury / fitness / condition / morale / form | פציעה / כושר / מצב גופני / מורל / כושר (form) |
| attributes / ability / potential | תכונות / יכולת / פוטנציאל |
| press conference / media / journalist | מסיבת עיתונאים / תקשורת / עיתונאי |
| youth intake / academy | מחזור נוער / אקדמיה |
| Player of the Month / Manager of the Year | שחקן החודש / מאמן השנה |
| Champions League / Europa League / Premier League | ליגת האלופות / הליגה האירופית / הפרמייר ליג |
| home / away / draw / win / loss | בית / חוץ / תיקו / ניצחון / הפסד |

## Style
- Numbers and token order follow Hebrew word order; never leave English words except names and acronyms
  (FIFA, UEFA, xG, VAR).
- Headlines short and punchy; commentary present tense ("[%male#1] בועט... גול!").
- Writing direction: write logical Hebrew; the build wraps every string in RLI…PDI for the UI.

## Decided during the UI pass (use these)
- A team/club name is grammatically feminine singular: "[%team#1-short] ניצחה", "שחקני [%team#1-short]".
- away goals שערי חוץ; on aggregate בתוצאה המצטברת; penalty shootout דו-קרב פנדלים; counter-attack מתפרצת;
  equalise השוותה; pull one back צימקה; go through עלתה שלב; six-pointer קרב (תחתית/צמרת).
- post קורה; bar משקוף; woodwork מסגרת; header נגיחה; cross הגבהה; yards יארד.
- shortlist רשימת מעקב; buy-back clause סעיף רכישה חוזרת; affiliate club מועדון שותף; licence רישיון.
- MLS: draft דראפט; trade טרייד.
- final day המחזור האחרון; transfer embargo עיצום העברות; feeder club מועדון בת; B team קבוצת B;
  dressing room חדר ההלבשה; pressing intensity עוצמת לחץ; pre-season הכנה לעונה; work permit אישור עבודה;
  conversion rate אחוז ניצול; touchline shout צעקה מהקווים; continental qualification העפלה למפעל יבשתי (not "אירופי": FM has every continent).
- "The board" (ההנהלה) is feminine singular: ההנהלה מרוצה / מודאגת.
- Staff: Data Analyst אנליסט נתונים; Sports Scientist מדען ספורט; Head of X ראש X; Chief X X ראשי.
- home grown מגידול עצמי; part exchange עסקת חילוף; future fee תשלום עתידי; key passes מסירות מפתח;
  interceptions חטיפות; treble / double טרבל / דאבל; fitness test מבדק כושר; left/right/both footed שמאלי/ימני/דו-רגלי;
  social posts: BREAKING מבזק, hashtags in Hebrew.
- backroom staff צוות מקצועי; caretaker manager מאמן זמני; set-piece routine תרגיל; versus נ'.
- Promise titles and history items: noun / infinitive forms.
- MLS: Designated Player שחקן מיועד; salary cap תקרת שכר; allocation הקצאה; international slot מכסת זר.
- aggregate (two legs) בתוצאה המצטברת; shootout דו-קרב פנדלים; drop zone אזור הירידה; runners-up סגנית.
- trial / trialist מבחן / שחקן במבחן; in administration בכינוס נכסים; financial fair play הגינות פיננסית;
  points deduction הורדת נקודות; tempo קצב; defensive line קו הגנה; team shape מבנה קבוצתי; own goal שער עצמי.
- Live commentary in present tense, match reports in past tense. Ages: עד גיל 21 (short: עד 21).
- Team nicknames ([%team#N-nickname]) take plural: "[%team#1-nickname] עולים".
- Number variants: -text -> [%number#N]; -nth -> "מקום [%number#N]" / "ה-[%number#N]".
- Fan social posts: spoken, first person male fan ("לא יכול לחכות"), hashtags with underscores (#העונה_המושלמת).
- derby דרבי; six-pointer משחק שש נקודות; run-in הישורת האחרונה; relegation battle המאבק בתחתית;
  unbeaten run רצף ללא הפסד; winless run רצף ללא ניצחון; instalments תשלומים; squad depth עומק הסגל.
- Nation tokens: prefer constructions that need no adjective agreement ("ה-[%nation#1-nationality]").
- Abbreviations use Hebrew gershayim ״ (מנכ״ל, סה״כ); keep the source's escaped \" and \n as they are.
- Position codes: שוע / מג / קה (defensive mid) / קש / קא (attacking mid) / חל; sides ימ / שמ / מר.
- goal types: volley וולה, chip צ'יפ, lob לוב, screamer טיל, diving header נגיחה בשלונג, overhead kick בעיטת מספרת.
- kick-off שריקת פתיחה; sell-on clause סעיף מכירה עתידית; reserves מילואים.
- in / out of possession עם כדור / ללא כדור; loan-to-buy השאלה עם אופציית רכישה; on international duty בשירות הנבחרת;
  tactical tweak כוונון טקטי (tweaks כוונונים); player/position instructions הוראות אישיות / הוראות עמדה.
- expected goals שערים צפויים (xG stays); expected assists בישולים צפויים; clear-cut chances מצבים ודאיים;
  possession won/lost זכיות בכדור / איבודי כדור; target forward חלוץ מטרה; match sharpness חדות;
  analyst אנליסט; Data Hub מרכז הנתונים; chairperson יו"ר; per game "/מש", per 90 "/90".
- Analyst remarks about a player: noun phrases (work for male and female players). Player replies to the
  manager avoid gendered address ("בוא").
- Club Vision חזון המועדון; Loan Manager מנהל השאלות; knockout stage שלב הנוקאאוט; continental competitions
  מפעלים יבשתיים; fatigue עייפות; mentoring חניכה; reputation מוניטין; terracing יציעי עמידה; loan back השאלה חוזרת.
- A team name takes a feminine singular verb ("[%team#1-short] לוחצת"); in commentary a plural pronoun for the
  team ("הם לוחצים") is fine when no name is used.
- Training: הגנה טקטית / אימוני הגנה טקטית / מאמן הגנה טקטית; goalkeeping שוערות / אימוני שוערים / מאמן שוערים.
- counter-press לחץ נגדי; overlap / underlap חפיפה / חפיפה פנימית; Gegenpress גגנפרסינג; Low Block בלוק נמוך; Park the Bus חניית האוטובוס.
- squad status: Fringe Player שחקן שוליים; Regular Starter פותח קבוע; Impact Sub מחליף משנה משחק.
- zonal/man marking שמירה אזורית / אישית; near/far post קורה קרובה / רחוקה; progressive passes מסירות מתקדמות;
  final third השליש האחרון; open play משחק פתוח; intermediary מתווך.
- Formations keep digits, words translated: "4-2-3-1 קשר אחורי רחב" (DM קשר אחורי, AM קשר התקפי, WB מגני כנף, Diamond יהלום).
- caps הופעות בנבחרת; workload עומס; prospects כישרונות; average rating ציון ממוצע; per week לשבוע.
- Team talks: spoken plural to the players (תמשיכו); manager's own words gender-neutral (מצפה, מרוצה, גאה).
- decider משחק ההכרעה; at stake על הכף; build-up בניית משחק; transition מעבר; GK distribution הוצאת השוער.
- cup draw pot קבוצת דירוג; scouting range טווח סקאוטינג; homegrown short ג"ע; wide centre-back בלם צד.
- Achievements to the manager: past-tense 2nd person without niqqud (ניצחת, זכית) reads for both genders.
- Data/Transfer/Competition Hub מרכז הנתונים / מרכז ההעברות / מרכז המפעלים; heat map מפת חום;
  switch of play החלפת אגף; Team of the Week נבחרת המחזור; tactical effectiveness אפקטיביות טקטית.
- (Player) Buy-In מחויבות (השחקנים); low/mid block בלוק נמוך / בינוני; progression התקדמות; Gameweek מחזור;
  International Management אימון נבחרות; Squad Planner מתכנן הסגל.

## Lessons from the review of the first bulk batch (follow strictly)
- No ה- before a token that prints a name or phrase: not "במשחק ה-[%fixture_name#1-long]" but
  "במשחק [%fixture_name#1-long]" / "במסגרת [%fixture_name#1-long]". Same for `[%conditions_description#N...]`
  and `-time_of_day_only` (write "ב-[...]" only where "ב" + the printed word is correct Hebrew; when unsure,
  rephrase so the token stands alone).
- `[%person#N]` in a text WITHOUT a gender split must stay gender-neutral: no "[%person#1] היה", "יהפוך לשחקן".
  Rephrase around a noun or infinitive ("תשומת הלב התמקדה ב-[%person#1]"). If that is impossible, the unit
  should have been a split: then use [%male#N]/[%female#N] wording in the m/f variants you output.
- No English calques in reports: write active Israeli sports Hebrew. Not "נהנתה מניצחון", "הובסה על ידי",
  "להוסיף סבל לעונה", "הניצחון היה מגיע ל-"; but "ניצחון נוח ומוצדק של", "ספגה תבוסה קשה מול",
  "ספגה הפסד ברור", "להעמיק את המשבר".
- Read every sentence back for meaning: numbers attach to the right noun ("לא ספג שער כבר [%number#1] דקות"),
  "otherwise good" = "שהייתה טובה בסך הכול", and every verb has its object.
- weaker foot הרגל החלשה; favourite הפייבוריטית; underdog בעמדת נחיתות / האנדרדוג; reach a final תופיע בגמר.
- More calques to avoid (review 2): "תשייט לניצחון" -> "תנצח בקלות"; "אוויר של אופטימיות" -> "שוררת אופטימיות";
  "מאבק מרים" (uphill struggle) -> "משימה קשה מאוד"; "שורר רושם כללי" -> "התחושה הכללית"; "היה יוצא דופן במספר
  העבירות" -> "התאפיין בריבוי עבירות"; "לא נפגע בסיכויים" -> "רק נשפר את הסיכויים"; second favourites -> "לא
  הפייבוריטית"; crucial game -> "המשחק המכריע" (דו-קרב = a two-legged tie only); keen (eager) -> "נחושים / להוטים";
  tight marking -> "שמירה צמודה". Watch which noun a pronoun or suffix refers back to.

- Spot check rest-062..086: in Manager Persona news an unsplit [%person#1] never gets "כמאמן/למאמן החדש" or "המאמן מ-X צפוי"; write "מינוי [%person#1] לתפקיד המאמן", "המינוי צפוי". No feminine-only predicate after a stand-in noun (הדמות ... כמנהיגה). UI terms inside sentences: שאינם מהאיחוד האירופי, להוציא את הכדור (GK), חוסר שביעות רצון.

## Idiom table (grows with every review; never translate these word for word)
| English | Hebrew |
|---|---|
| uphill struggle / uphill task | משימה קשה מאוד / מאבק קשה |
| cruise / sail to victory | ניצחון קל / ניצחה בקלות |
| enjoy a win | ניצחה / רשמה ניצחון |
| be beaten by / be thrashed by | הפסידה ל- / ספגה תבוסה מול |
| add to the misery | להעמיק את המשבר |
| otherwise good (performance) | (הופעה) שהייתה טובה בסך הכול |
| second favourites | לא הפייבוריטית / המועמדת השנייה |
| crucial game / decider | המשחק המכריע |
| keen to (eager) | נחושים / להוטים |
| tight / close marking | שמירה צמודה |
| an air of optimism | שוררת אופטימיות |
| the general feeling in the camp | התחושה הכללית במחנה |
| the game was notable for fouls | המשחק התאפיין בריבוי עבירות |
| it won't hurt our chances | זה רק ישפר את הסיכויים שלנו |
| must-win game | משחק שחייבים לנצח |
| game in hand | משחק אחד פחות / משחק חסר |
| transfer-list a player | להעמיד למכירה |
| comeback trail | מסלול חזרה |
- Manager's own first person: same-spelling forms only (רוצה, מקווה, מרוצה, גאה, לדעתי, נראה לי) so it fits a
  male or female manager; questions to the manager in plural (אתם, מה דעתכם). Manager headlines:
  "[%person#1-surname]: <noun phrase>". goal kick בעיטת שוער; complacency שאננות; cup upset הפתעת הגביע.
- stoppage time תוספת זמן; possession החזקת כדור; relegation zone אזור הירידה; promotion places מקומות העלייה.
- Never write {a|b} alternatives: FM has no such syntax. Gender goes in the m/f variants.
- Prefix letters before ANY token stay hyphenated ("ב-[%nation#1]", "ה-[%nation#1-nationality]"): nation and
  team names may print in English (from the database), so "ב-Arsenal" must work. Avoid adjective agreement
  with -nationality where you can ("העיתונות ב-[%nation#1]").
- touchline ban איסור לשהות על הקווים; six-pointer קרב תחתית/צמרת.
| bragging rights (derby) | הכבוד בעיר / הזכות להתגאות (not "זכות ההתרברבות") |
| see out the result | לשמור על התוצאה |
| help from elsewhere (other results) | עזרה ממגרשים אחרים |
| relegation playout | פלייאוף הירידה |
| second leg | המשחק השני / משחק הגומלין |
| numerical advantage | יתרון מספרי |
| goal difference | הפרש השערים (not "יחס השערים") |
| cup upset (cupset) | סנסציית גביע / הפתעת הגביע |
| holders | המחזיקה בתואר |
| hair-dryer treatment (team talk) | שטיפה בחדר ההלבשה / צעקות בחדר ההלבשה (not "מייבש השיער") |
| scapegoat | שעיר לעזאזל |
| gutted / distraught | שבור / מרוסק |
| half-chances | חצאי מצבים |
| takeover / buy-out | השתלטות / רכישת השליטה |
| administrators (insolvency) | כונסי נכסים |
| supporters' trust | אגודת האוהדים |
| replay / return leg | משחק חוזר / משחק הגומלין |
| season ticket | כרטיס עונתי |
| gate receipts | הכנסות ממכירת כרטיסים |
| Surely ...? (media question) | ...ודאי ..., לא? / ...הרי ..., נכון? (not "בוודאי ...?") |
| are you confident of ...? | אתם בטוחים ש...? (not "יש לך ביטחון ל...") |
| how do you see the result going? | איך לדעתכם המשחק ייגמר? |
| get something out of the game | לצאת עם משהו מהמשחק |
| do you share the view that | אתם שותפים לדעה ש... |
| there for the taking | בהישג יד |
| not get ahead of ourselves | לא להיסחף |
| (goal) should have stood | אף שהיה צריך לאשר אותו |
| chasing shadows | רדפה לשווא אחרי הכדור |
| put their bodies on the line | זרקו את עצמם לחסימות |
| I'd be lying if I said | אשקר אם אומר (not "הייתי משקר") |
- Tokens that print OUR OWN Hebrew strings ([%job#N], [%position#N...], [%tactical_role#N], [%injury#N],
  [%foul#N], [%basic_goal_description#N], [%conditions_description#N]) take prefix letters
  directly, WITHOUT a hyphen: "ה[%job#1]" -> המאמן, "ב[%position#1-lowercase]". Names that may print in
  English (team, person, nation, comp, award, stadium, city, fixture_name) keep the hyphen: "ב-[%team#1-short]".
- Split units: the m/f split is about ONE person (the one the English pronouns refer to). In the m variant mark
  that person [%male#N...], in the f variant [%female#N...]; every other person stays [%person#N...] (or
  [%person#N-hidden]) and is written gender-neutral. Never mark the manager male/female unless the split is
  about the manager.
- The manager's first person: also avoid masculine-only forms like אני מאחל, די בטוח, הייתי אומר; use לדעתי,
  נראה לי, אשמח, אני בטוח/ה -> "ברור לי".
| lucky breaks | היה לנו מזל בכמה רגעים |
| gave them a game | נתנו להם פייט |
| did themselves justice | הראו את היכולת האמיתית שלהם |
| more than a match for | חזקה מהם בהרבה |
| upturn in fortunes | מגמה חיובית |
| title credentials | מועמדת אמיתית לתואר |
| move on from | לשים מאחור את |
| tore up the script | טרפה את הקלפים |
| smash and grab victory | גנבה ניצחון |
| a class apart | בליגה אחרת |
| could count themselves fortunate | יכולה לברך על מזלה |
| not much love lost between | היחסים ביניהם קרירים |
| upset the odds | הפתיעה את כולם |
| mid-table obscurity | אפרוריות באמצע הטבלה |
| pundit / bookmakers | פרשן / סוכנויות ההימורים |
| for all the wrong reasons (headlines) | יעלה לכותרות, ולא מהסיבות הטובות |
| at the end of the day | בסופו של דבר (not "בסוף היום") |
| if anything | אם כבר |
| there and then | באותו רגע (not "שם ואז") |
| it just wasn't to be | זה פשוט לא היה בקלפים |
| on the wrong end of a hiding | ספגה תבוסה |
| managerial master stroke | מהלך גאוני |
| prove the doubters wrong | הוכיחה לספקנים שהם טעו |
| deserved to win | הגיע להם לנצח / ניצחון מוצדק |
- Line breaks: copy the English form exactly. Where the English has the two characters backslash + n, write
  backslash + n (in Python source: "\n"), never a real line break.
| VAR was a factor | ה-VAR מילא תפקיד |
| otherwise unremarkable | שהייתה חסרת ייחוד בסך הכול |
| glimmer of hope | זיק של תקווה |
| harsh (decision) | חמור מדי |
| clear and obvious (error) | ברורה ומובהקת |
| uphold a decision | השאיר את ההחלטה על כנה |
| it is what it is | זה מה יש |
| back to the drawing board | להתחיל הכול מאפס |
| a good day at the office | יום עבודה טוב |
| had a let-off | יצאנו בזול |
| in the back of my mind | בראש שלי / מאחורי הראש (not "בראש מעייניי") |
| won headers | נגיחות שנוצחו |
| form is temporary, class is permanent | כושר הוא זמני, איכות היא נצחית |
| the proof is in the pudding | המבחן האמיתי הוא על המגרש |
| take the game to them | לעלות עליהם מההתחלה |
| what the form book says | על הנייר |
| knocked them off their feet | הכניס אותם להלם |
| out of order / out of line | חצה את הקו |
| X minutes in | אחרי X דקות (not "X דקות לתוך המשחק") |
| right the ship | לחזור למסלול |
| good luck | בהצלחה (מזל טוב = congratulations) |
| could be serious (injury) | עלולה להיות חמורה |
| build on (a result/run) | להמשיך את המומנטום / לנצל את (not "לבנות על") |
| it's going to be (tough) | זה יהיה (קשה) (not "זה הולך להיות") |
| put on a show | לתת הצגה |
| not the be-all and end-all | זה לא חזות הכול |
| it's not about him | זה לא תלוי בו |
| this result is on them | התוצאה הזאת עליהם (their fault) |
| gave everyone a lift | נתן לכולם זריקת עידוד |
| run rings around them | נריץ אותם על המגרש |
| impose ourselves | להכתיב את הקצב (not "לכפות את עצמנו") |
| stretch ourselves | לאתגר את עצמנו |
| over the moon | בעננים (not "על הירח") |
| went out of the window | ירד לפח |
| not least because | ולו רק כי |
| make no mistake | שלא יהיה ספק |
| can't begrudge him | אי אפשר לבוא אליו בטענות |
| treasure (a moment) | ינצור |
| roar back | חזרה בסערה |
| bad day at the office | יום חלש |
| plays right into our hands | זה רק משחק לטובתנו |
| at worst | במקרה הגרוע |
| grow complacent | להיכנס לשאננות (not "להפוך שאננים") |
| up against it | צפויה לנו משימה קשה |
| a different proposition | סיפור אחר לגמרי |
| we're there to be shot at | כולם רוצים להפיל אותנו |
| run through brick walls | לתת את הנשמה על המגרש |
| our hands full | מחכה לנו עבודה קשה |
| record (won-lost record) | מאזן (not "שיא") |
| when all is said and done | בסופו של דבר |
| translate into a win | להפוך לניצחון / להניב ניצחון |
| clears his lines | מרחיק את הסכנה |
| trip (foul) | הכשלה |
| that was inspired | רגע גאוני |
| untouchable (player) | אי אפשר לעצור אותו/ה |
| slip up (rivals) | ימעדו |
| top of the table | במקום הראשון בטבלה (בצמרת = among the top places) |
| guaranteed the title if | תבטיח את התואר אם |
| rallied his team-mates | דרבן את חבריו |
| combine with (a team-mate) | לשלב משחק עם |
| caps the win | חותמת את הניצחון |
| show up and perform | להתייצב ולספק את הסחורה |
| penalties are a lottery | פנדלים זה לוטו |
| one hand on the trophy | יד אחת כבר על הגביע |
| make it happen | לעשות את זה (not "לגרום לזה לקרות") |
| build up their confidence | לחזק את הביטחון שלהם |
| champions in all but name | כמעט אלופים / למעשה אלופים |
| written us off | הספידו אותנו |
| almost there! | עוד קצת! |
| cause an upset | להפתיע (not "לגרום להפתעה") |
| results elsewhere | התוצאות במגרשים האחרים |
| hold your hands up and credit | לתת קרדיט (not "להרים ידיים" = surrender) |
| getting ahead of himself | נסחף |
| left to rue | מתייסר / מצטער על |
| would be an understatement | זו לשון המעטה |
| one yellow card away from a suspension | במרחק כרטיס צהוב אחד מהרחקה |
| run the clock down | לשרוף את השעון |
| fair share (of) | לא מעט |
| on N minutes | בדקה ה-N (not "עד הדקה") |
| set a record | קבע שיא (שבר שיא = broke a record) |
| baffled | מבולבלים (not "נבוכו") |
| final day | המחזור האחרון (not "יום המחזור האחרון") |
| it's as simple as that | וזה כל הסיפור |
| see what happens from there | ומשם נראה |
| keep pushing for | ממשיכים להילחם על |
| we're (the) favourites | אנחנו הפייבוריטים |
| see us qualify for X | יבטיח לנו העפלה ל-X (not "יעפיל אותנו") |
| I'm furious | אני בזעם |
| win the second half | לנצח במחצית השנייה |
| safe from relegation | הבטיחה את הישארותה בליגה |
| results elsewhere go our way | התוצאות במגרשים האחרים יהיו לטובתנו |
| seal (promotion / the title) | לסגור את העלייה / את האליפות (not "לחתום") |
| we should expect nothing less | לא נסתפק בפחות מזה |
| X means that we... | בזכות X אנחנו... (not "X אומר ש") |
| I'd be angry if I were you | במקומכם הייתי בזעם |
| come out on top | לצאת כשידנו על העליונה |
| one of the good people | מהאנשים הטובים בכדורגל |
| assert themselves | להכתיב את הטון |
| qualifying spot | מקומות ההעפלה |
| results go our way | התוצאות ייפלו לטובתנו (not "יתנו לנו יד") |
| make a difference | לעשות את ההבדל |
| let a chance go begging | להחמיץ את ההזדמנות |
| poor run of form | הרצף הרע |
| prove a point | להוכיח את עצמם |
| I'm disappointed that (manager) | מאכזב אותי ש... (not "האכזבה שלי גדולה") |
| push players forward | מעלה שחקנים להתקפה |
| it was one of those days | זה פשוט היה יום כזה |
| extra time | הארכה (תוספת הזמן = stoppage time) |
| middle section (split league) | הקבוצה האמצעית בפיצול הליגה |
| silky touch | נגיעה קטיפתית |
| a lovely bit of skill | מהלך מיומן ויפה |
| tough crowd | קבלת פנים קשה מהיציע |
| turn on you (fans) | לפנות נגדך |
| desperate to get a result | להוטים להוציא תוצאה |
| feed off (the crowd) | לשאוב מוטיבציה מ- |
| first-ever final | הגמר הראשון בתולדות המועדון |
| how did you feel about X? | מה דעתכם על כך ש...? |
| defended very well | הגנו מצוין |
| don't get complacent | אסור לנו להיכנס לשאננות |
| express yourselves | לשחק בחופשיות |
| the media have been on your backs | התקשורת לא מרפה מכם |
| we owe them one | יש לנו חשבון פתוח איתם |
| thorn in their side | לא נתן להם מנוח |
| get on the end of chances | מגיע למצבים טובים |
| contain (a player) | לנטרל |
| non-negotiable | שאין עליו ויכוח |
| tie (cup match-up) | מפגש / דו-קרב |
| pundits | פרשנים |
- Role nouns with NO person token (job titles in lists, award names, generic bios) may use the generic
  masculine (שחקן, מנכ"ל, מאמן). A [%person#N] / [%male#N] / [%female#N] in the sentence follows the gender rules.
| make the short trip to | תעשה את הדרך הקצרה ל- |
| come as a shock | יפתיע רבים |
| produce a shock | לחולל הפתעה |
| famous win | ניצחון היסטורי |
| unceremoniously dumped out | הודחה ללא רחמים |
| stern opposition | יריבות קשות |
| change hands (club) | לעבור לידיים חדשות |
| board takeover | חילופי בעלות במועדון |
| season ticket holders | בעלי כרטיסים עונתיים |
| win promotion | לעלות ליגה |
| talismanic (player) | השחקן הגדול שלה / עמוד התווך (not "הקמע" = mascot) |
| touch and go (injury) | בסימן שאלה |
| title decider | משחק ההכרעה על התואר |
| defensive record | המאזן ההגנתי |
| goal-scoring record | מאזן הכיבוש |
| grace (a club) | פעל ב- |
| keep the score down | להחזיק מעמד בפער קטן |
| staked a claim as one of the best | ביסס את מקומו בין הטובים ביותר |
| swept all before them | דרסה את כל מי שעמד בדרכה |
| not many will forget | מעטים שישכחו |
| unfortunate not to win | הייתה ראויה לנצח |
| the ban (suspension) | ההשעיה |
| saw a goal disallowed | שער של X נפסל |
| low point | נקודת השפל |
| play second fiddle | לשמש כינור שני |
| outspoken comments | דברים נחרצים / גלויים |
| hot on the trail of | במרדף צמוד אחרי |
| a report suggests that | לפי דיווח של ... |
| never been capped | אף לא הופעה אחת בנבחרת |
| N year-old (unsplit person) | בגיל N / (גיל N) (not "בן N") |
| unbeaten run | הרצף ללא הפסד |
| confound the critics | הוכיחה למבקרים שטעו |
| a remarkable N trophies | לא פחות מ-N תארים |
| first win in N games | הניצחון הראשון מזה N משחקים |
| taste defeat | ספגה הפסד (not "טעמה הפסד") |
| end on a high | לסיים בשיא |
| mid-table slog | לדשדש באמצע הטבלה |
| pinch a qualification spot | לגנוב מקום העפלה |
| pull the plug (on a deal) | לטרפד את העסקה (not "למשוך את התקע") |
| left them wanting more | השאירה טעם של עוד |
| earn maximum points | לקחת את שלוש הנקודות |
| winless streak | הרצף ללא ניצחון |
| squad numbers | מספרי החולצות |
| the stuff of nightmares | תרחיש בלהות |
| suffered an [%injury#N] | אחרי [%injury#N] / בעקבות [%injury#N] (injury names vary in gender) |
| rank outsiders | אנדרדוג מובהק |
| the jury is still out | מוקדם לשפוט |
| managerial hot seat | כיסא המאמן |
| favourite to get the job (unsplit person) | הסיכוי הגבוה ביותר לקבל את התפקיד הוא של X |
| position untenable | לא הייתה דרך להמשיך בתפקיד |
| move on to pastures new | פונה לדרך חדשה |
| putting the finishing touches to | משלימות את ההכנות האחרונות ל- |
| ... and scored in the process | ואף הבקיע |
| youngest ever goalscorer (unsplit person) | שיא לכיבוש שער בגיל הצעיר ביותר |
| looking to (win) | שואפת ל- (not "מחפשת ל-") |
| a situation not helped by X | מצב ש-X רק החמיר |
| hearts in their mouths | ליבם החסיר פעימה |
| from bad to worse | מרע לגרוע |
| biggest talking point | הרגע המדובר ביותר |
| rally (team) | תתגייס (not "תתאגד") |
| reserving judgment | עדיין לא מגבשים דעה |
| arrest a poor run | לבלום את הרצף הגרוע |
| not much to choose between | הפערים קטנים |
| forthcoming [comp] | [comp] שבפתח (gender of the comp name unknown) |
| make the cut (squad) | להיכנס לסגל (not "לעבור את החיתוך") |
| pushing for inclusion | דופקים על דלת הנבחרת |
| the pundits' favourite | הבחירה המועדפת על הפרשנים |
| coming through the youth system | בוגרי מחלקת הנוער |
| X understands that (media) | לפי המידע של X (not "X מבינה") |
| a welcome headache | כאב ראש מבורך |
| managers (football) | מאמנים (not "מנהלים") |
- The definite article goes on own-Hebrew tokens: "ה[%job#1] החדש", "ה[%position#1-lowercase] [%person#1]".
| off the pace | מפגרת אחרי הצמרת |
| generate X from player sales | להכניס X ממכירת שחקנים |
| splash the cash | פתחה את הארנק |
| followed up a draw with a win | אחרי תיקו ניצחה |
| overcame a defeat in style | מחקה בגדול הפסד |
| deducted N points | נענשה בהורדת N נקודות |
| proved to be their undoing | היא שהפילה אותם |
| stepped up | לקחו אחריות |
| arrivals / departures | הרכש / השחקנים שעזבו |
| on the same page | מדברים באותה שפה |
| high on the agenda | בראש סדר העדיפויות |
| compound the misery | המשבר העמיק |
| a step up the ladder | לעלות מדרגה |
| one of the signings of the season | אחת הרכישות הטובות של העונה |
| produce (youth players) | הצמיחה |
| borrow (loan) | מקבלת בהשאלה |
| the eventual champions | הקבוצה שזכתה בסוף בתואר |
| FFP total / limit | מגבלת ההגינות הפיננסית |
| X seconds into the match | אחרי X שניות בלבד |
| high-level concerns | בדרגים הבכירים חוששים |
| beleaguered (manager) | הנתון בלחץ כבד |
| overcame the longest of odds | נגד כל הסיכויים |
| foul-mouthed tirade | מטח קללות |
| who famously did X (unsplit bio) | לזכות X נזקף ש... |
| who are already without X | שכבר חסרים לה X |
| lift the trophy | הניף את הגביע / הנפת הגביע |
| [%media_source#N] reports (subject) | ב-[%media_source#N] מדווחים (source gender unknown) |
| few eyebrows have been raised | לא הפתיע כמעט איש (not "מעט גבות עלו") |
| stare relegation in the face | עומדת על סף ירידה |
| jump ship | לעזוב מיוזמתו |
| prise away (a player) | לחלץ את X מהמועדון |
| disciplinary record | מאזן המשמעת |
| yellow card tally | מספר הכרטיסים הצהובים |
| a blip | מעידה חד-פעמית |
| there were joyous scenes | השמחה הייתה גדולה |
| non-playing roles | תפקידים מחוץ למגרש |
| my bread and butter | הבית שלי / מה שאני עושה הכי טוב |
| wouldn't touch it with a barge pole | בשום מחיר |
| chastening experience | חוויה מפכחת |
| crisis point reached | המשבר הגיע לשיאו |
| local investor [%person#N] | [%person#N], מבעלי ההון המקומיים |
| goalkeeper [%person#N] (unsplit) | [%person#N] בין הקורות |
| homegrown contingent | מספר השחקנים מגידול עצמי בסגל |
| disbelief | תדהמה |
| lost in the final | הפסידה בגמר (not "הודחה") |
| backed up his interest publicly | הביע בפומבי את העניין שלו |
| ruled himself out (of a job) | הוציא את עצמו מהמרוץ |
| add fuel to suggestions | מחזק את ההשערות |
| market favourite (for a job) | הפייבוריט של סוכנויות ההימורים |
| caused a stir | עורר סערה |
| play down speculation | הפחית מחשיבות הספקולציות |
| dip into the loan market | פנה לשוק ההשאלות |
| marquee signing | רכש כוכב |
| take heart from | לשאוב ביטחון מ- |
| after all | אחרי הכול (בסך הכול = all in all) |
| are at it again | חוזרת לסורה |
| break the bank | לפתוח את הכיס |
| didn't set the world alight | לא הותיר רושם מיוחד |
| short but sweet | קצרה אך מוצלחת |
| it is generally accepted that | הדעה הרווחת היא ש |
| keep cards close to the chest | לשמור את הקלפים קרוב לחזה |
| transfer coup | הישג ענק בשוק ההעברות |
| mouth-watering tie | מפגש מסקרן במיוחד |
| special praise for | מגיעים שבחים מיוחדים ל- |
| retain the trophy | להגן על התואר |
| high-flying / high-fliers | קבוצת הצמרת |
| [comp] defence (holders) | ההגנה על התואר ב-[comp] |
| blow it / bottle it | לפשל / להתפרק |
| push on | להמשיך בכל הכוח |
| former manager [%person#N] (unsplit) | [%person#N], פנים מוכרות מהספסל שלנו |
| go top | לעלות למקום הראשון |
| tantalisingly close to | במרחק נגיעה מ- |
| in the driving seat | בעמדת שליטה |
| drown one's sorrows | להטביע את הצער |
| successes (titles) | זכיות |
| didn't deserve to see that | לא הגיע להם לראות את זה |
| leaves a lot to be desired | יש עוד הרבה מה לשפר |
| X will be kicking themselves | ב-X בטח אוכלים את הלב |
| feel sick to my stomach | הבטן שלי מתהפכת |
| freak result | תוצאה הזויה |
| was always going to be tough | היה ברור שיהיה קשה |
| can't believe the spirit in this team | לא ייאמן איזו רוח יש בקבוצה הזאת |
| be the bigger people | להתעלות מעל זה |
| relieved | הוקל לי (not "נרגע") |
| who cares | למי אכפת |
| go away and think of what might have been | תישאר לתהות מה היה יכול להיות |
| extraordinary doesn't begin to cover it | "יוצא דופן" זו לשון המעטה |
| let that sink in | תחשבו על זה רגע |
| the team to beat | הקבוצה שכולם ירצו להפיל |
| emerge from the pack | לפרוץ מהגוש |
| defied expectations | התעלתה על התחזיות |
| fell agonisingly short | נגמר במרחק נגיעה |
| a season of what-ifs | עונה של החמצות |
| what a time to be a supporter | איזו תקופה להיות אוהד |
| an incredible N trophies | לא פחות מ-N תארים |
| jump ship (manager/player) | לנטוש בהזדמנות הראשונה |
| had his head turned | התפתה להצעות אחרות |
| a steady pair of hands | יספק יציבות |
| amazing scenes | רגעים מדהימים (not "תמונות מדהימות") |
| early bath | הרחקה |
| U-turn | פניית פרסה |
| can't believe X has left (unsplit) | לא מאמין לעזיבה של X |
| with class and dignity | באצילות ובכבוד |
| play me or sell me | תנו לי לשחק או תמכרו אותי |
| promoted to manager | קודם לתפקיד המאמן |
| we welcome X to the final | X מגיעה לגמר |
| fascinating to discover why | מסקרן מאוד לדעת למה |
| big shoes to fill | יהיה קשה למלא את החלל |
| step up to replace X | ייכנס לנעליים של X |
| that was never a red | זה בשום אופן לא היה אדום |
| give me a break! | עזבו אותי! |
| our first-ever final | הגמר הראשון בתולדותינו |
| produce (players) | הצמיח (not "הוציא" / "הפיק") |
| player-manager | שחקן-מאמן / שחקנית-מאמנת |
| lino | הקוון |
| (senior) debut | בכורה (בוגרת) |
| all-time top scorer (national team) | מלך / מלכת השערים של הנבחרת |
| rightfully aggrieved | מקופח בצדק |
| bit-part player | שחקן שוליים |
| over the moon / chuffed to bits | בעננים |
| poor run | הרצף הגרוע |
| heavy defeat | הפסד כבד / תבוסה מוחצת |
| failing to report for training | אי-התייצבות / היעדרות |
| relegation six-pointer | קרב תחתית |
| touch and go | בסימן שאלה |
| first-choice keeper | שוער / שוערת הבחירה הראשונה |
| Player Status Committee | ועדת מעמד השחקנים |
| pre-contract | הסכם קדם-חוזה |
| Joker window | חלון הג׳וקר |
| cash in on (a player) | לגזור קופון על |
| all sorts of nervous | מלחיץ אותי ברמות |
| roll over and hand (the title) to | להרים ידיים ולהגיש על מגש ל- |
| asking for trouble | מתכון לצרות |
| a mixed bag (recent years) | פעם כך ופעם כך |
| I'll take that (satisfied) | מקבל את זה בשמחה |
| one I can take or leave | לא חם ולא קר לי לגבי זה |
| Never in doubt? | היה ספק בכלל? |
| keep the opposition guessing | להפתיע את היריבות |
| suffered the agony of defeat | ספגה הפסד כואב |
| I'm in the business of winning | התפקיד שלי הוא לנצח |
| campaign (season) | העונה / הדרך (not "המסע") |
| Talk about defying the odds! | נגד כל הסיכויים! |
| long may it continue | שיימשך ככה עוד הרבה זמן |
| let alone (a backup) | קל וחומר (בשביל שחקן ספסל) |
| we're only a good run away from X | רצף טוב אחד ו-X |
| would go a long way to securing it | יקרב אותנו מאוד לזכייה בו |
| fall short (fan post) | ניפול בדרך (not "נישאר קצרים") |
| a dubious run of form | ירידה מדאיגה בכושר |
| knee-jerk reaction | תגובה פזיזה |
| small-time (to celebrate) | קטנוני |
| permanent clause (loan) | אופציית רכישה |
| in the driving seat | בעמדת שליטה |
| the jury is still out | מוקדם לשפוט |
| For a match which promised so much | במשחק שהבטיח כל כך הרבה (not "למשחק ש...") |
| low-key affair | משחק אפור |
| damp squib | אכזבה גמורה |
| will be debated for a while yet | עוד יתווכחו על זה זמן רב |
| They didn't get the result but | התוצאה אמנם לא הגיעה, אבל |
| jubilant scenes at X | שמחה גדולה ב-X |
| get over the line (promotion) | סגרה את העלייה |
| went toe-to-toe | נלחמו ראש בראש |
| treated harshly (dismissals) | נענשה בחומרה מופרזת |
| current/previous manager [%person#N] (unsplit) | בקדנציה (הקודמת) של [%person#N] |
| testimonial match | משחק הוקרה |
| minimum fee release clause | סעיף שחרור במחיר מינימום |
| recall from loan | להחזיר מההשאלה |
| take off the transfer list | להסיר מרשימת המכירה |
| opened the scoring | פתח את התוצאה |
| it was worth the wait for X | היה שווה לחכות ל-X |
| I'm done (fan quitting) | מבחינתי זה נגמר |
| to be honest | למען האמת (not "ביושר") |
| one to watch (team) | קבוצה ששווה לעקוב אחריה |
| do them proud | יגרום להם להתגאות |
| survive the drop | נשארה בליגה |
| trade down (draft) | לרדת בסדר הבחירות בטרייד |
| don't immediately come across as | על פניו לא נראים כ- |
| prohibitive (cost) | יקר מדי |
| allay fears | להפיג חששות |
| impressive season (stat bio opener) | עונה מרשימה של X (not "הופעה מרשימה של X ... ב-N הופעות") |
| VAR became a factor / was involved | ה-VAR מילא תפקיד / היה מעורב |
| came under scrutiny (VAR) | היה תחת זכוכית מגדלת |
| throw caution to the wind | זנחו כל זהירות |
| the stuff of legend | נכנס לפולקלור |
| run of N consecutive titles | רצף N האליפויות (not "רצף N התארים ברציפות") |
| the chasing pack | הקבוצות הרודפות |
| mount a (serious) challenge / concerted bid for | להילחם (ברצינות / בכל הכוח) על |
| keep afloat (relegation) | לשרוד / במאבק לשרוד |
| reduced to a bitter joke | יהפוך לבדיחה מרה |
| carelessly dropped points | נקודות שאיבדנו ברשלנות |
| goal disallowed | השער לא אושר (not "לא נפסק") |
| physio: X has suffered [%injury] | פציעה של ה[%position] X: [%injury] (injury names differ in gender) |
| (relative) outsider for the job | סיכוייו לקבל את התפקיד קלושים / נמוכים יחסית (not "מועמד חיצוני") |
| glittering array of silverware | ארון התארים המפואר |
| intense media speculation | גל של ספקולציות בתקשורת |
| increasingly comfortable with the idea | מתחברים יותר ויותר לרעיון |
| managerless [team] | [team], שנותרה ללא מאמן, |
| much-vaunted (policy) | המדוברת |
| punching above their weight | מקומה גבוה בהרבה ממה שמצופה ממנה |
| playing career (unsplit person) | קריירת המשחק של X |
| would consider it a big step down | יראה בזה צעד גדול לאחור |
| concerned (fans) | המודאגים (never "החרדים") |
| revenue | הכנסות / מכניסה (not "מרוויחה") |
| waiver (MLS) / waive | ויתורים: הוצא לוויתורים, רשימת הוויתורים, דראפט הוויתורים (not "ווייבר") |
| Targeted / General Allocation Money | כספי הקצאה ממוקדת / כללית |
| got on the scoresheet | כבש |
| laid on (N goals) | בישל |
| through the pain barrier | למרות הכאבים |
| icing on the cake | הדובדבן שבקצפת |
| buy-back option | אופציה לרכישה חוזרת |
| tremendous start | פתיחה אדירה |
| beat all the odds to (win / promotion) | ... נגד כל הסיכויים |
| done X proud | הסב גאווה ל-X |
| one of the very best in the game | אחד הטובים ביותר בענף (not "במשחק") |
| hold up their end of the bargain | עמדו במשימה |
| on the wrong end of results | ספגה תוצאות |
| continue to be a success for the club | ימשיך להצליח במועדון |
| not on the cards | לא נראה אפשרי |
| less than forthcoming | לא שיתף פעולה |
| super-sub inspires/rescues (unsplit) | כניסת זהב של X מהספסל מציתה / מצילה את... |
| miracle worker | מחולל / מחוללת ניסים |
| pull the plug | טרפד / ביטל |
| fell just short (title) | החמיצה אותו בהפרש זעום |
| takeover saga continues to drag on | הסאגה ממשיכה להתארך |
| potential milestone | ההישג האפשרי / השיא |
| captured the imagination of | הלהיבה את |
| tantalisingly close to | במרחק נגיעה מ- |
| mid-season wobble / hiccup | מעידה באמצע העונה |
| make a bold statement (club) | שלחה מסר נועז |
| mean business | לא באה לשחק |
| groups (takeover bidders) | גורמים / קונסורציום (not "קבוצות") |
| sensationally quashed reports | בהפתעה גמורה הכחישה את הדיווחים |
| managerial hot seat | כיסא המאמן (not "הכיסא החם") |
| steady the ship | להחזיר את היציבות |
| paid immediate dividends | השתלמה מיד |
| hardly proved catastrophic | לא הייתה הרת אסון |
| has the Midas touch | כל מה שהוא נוגע בו הופך לזהב |
| entertainment on display | הכדורגל המהנה שהקבוצה מציגה |
| fierce rival | יריבה מושבעת |
| well-regarded | המוערך (not "הידוע לכול") |
| would be a squad / backup player (unsplit scout) | חלק מהסגל / תפקיד של גיבוי |
| under new manager [%person#1] (unsplit) | תחת ההדרכה החדשה של [%person#1] |
| upper echelons of the league | צמרת הליגה |
| title credentials | מועמדת אמיתית לתואר |
| an air of optimism | שוררת אופטימיות |
| VAR-affected match | משחק שהושפע מה-VAR |
| triumph over adversity | ניצחה על אף כל הסיכויים |
| shop window | חלון הראווה |
| obligation to buy | חובת רכישה |
| loan fee | דמי השאלה |
| fan mood ladder | בעננים > מאושר > שמח מאוד > מרוצה מאוד > שמח > מרוצה > די מרוצה > שבע רצון; כועס > זועם; מאוכזב עד כאב; מבולבל |
| occasional reluctance to (unsplit) | חוסר הנכונות שמגלה X מדי פעם ל- |
| apparent objection | ההתנגדות המסתמנת |
| slight lack of experience | ניסיון מועט יחסית |
| considerable lack of experience | ניסיון דל |
| in rude health | נראה איתן מתמיד |
| eyebrows have been raised at | עורר פליאה |
| change of fortune (for the better) | תפנית לטובה |
| discussions will continue at board level | בהנהלה ימשיכו לדון |
| will be sidelined with [%injury#N] (unsplit) | בשל [%injury#N], צפויה ל-X היעדרות מהמגרשים |
| glut of goals | מבול שערים |
| entertaining football / entertain | כדורגל מהנה / לבדר (not "משעשע") |
| have been quite open about | לא הסתירה את |
| will be pleased at boardroom level | בהנהלת X ודאי מרוצים |
| doesn't immediately appear to | על פניו ... לא |
| we're on to something here | נראה לי שמצאנו פה משהו |
| big fan of (fan post) | מת על (not "מעריץ גדול של") |
| wage contribution (loan) | השתתפות בשכר |
| wage bill | הוצאות השכר |
| General Allocation Money | כספי הקצאה כללית |
| a slew of (deals) | שורה ארוכה של |
| Not too soon either | והגיע הזמן |
| made headlines by promising | עלה לכותרות כשהבטיח |
| scale back ambitions | להנמיך את השאיפות |
| saw off competition at the ballot box | גבר בקלפי על |
| biggest spenders (transfer window) | המועדונים שהוציאו הכי הרבה כסף |
| respect is a two-way street | כבוד צריך להיות הדדי |
| consolidate debts | איחוד חובות |
| blessing in disguise | ברכה במסווה |
| we can do better (fan) | אפשר למצוא יותר טוב |
| have our eyes on (targets) | עוקבים אחרי |
| cross that bridge when we come to it | נתעסק בזה כשנגיע לשם |
| don't hold your breath | לא כדאי לבנות על זה |
| on the same page | מדברים באותה שפה (not "באותו עמוד") |
| strike while the iron is hot | להכות בברזל בעודו חם |
| kick-start (a season) | להתניע מחדש |
| have the edge over | מחזיקה ביתרון על |
| leave under a cloud | לעזוב בנסיבות עכורות |
| (official) had a nightmare | השופט היה אסון מוחלט |
| pass a fitness test | עמידה במבדק הכושר (not "מעבר") |
| nature of the beast | ככה זה בכדורגל של היום |
| ready to unleash | מוכן לשלוף / להציג (not "לשחרר") |
| sitting Nth (in the table) | היה במקום N (not "ישב במקום") |
| out in the cold (left out) | ממשיכה להתעלם מ- (not "הכתף הקרה") |
| team only qualifying for the playoffs | קבוצה שהעפילה רק לפלייאוף |
| team and competition records | שיא מועדון ושיא מפעל |
| set a new milestone | יקבע שיא חדש |
| exceeded expectations | עלתה על כל הציפיות |
| next edition of [comp] | [comp] של העונה הבאה (not "המהדורה הבאה") |
| balance the books | לאזן את התקציב |
| kickabout | כדורגל שכונתי |
| loaned in (player) | לקבל בהשאלה (not "להשאיל") |
| minor force (nation) | נבחרת שולית יחסית |
| duly crowned | הוכתרה כמצופה |
| avoid receiving a fine (board target) | שהקבוצה לא תקבל קנס |
| panic buy | רכש בפאניקה |
| didn't tick all the boxes | לא ענה על כל הצרכים |
| so close they can almost taste it | כבר מרגישה אותה בקצות האצבעות |
| deal falls apart (headline) | העסקה מתפוצצת |
| home-grown (unsplit) | תוצרת בית של המועדון |
| Well up for it! (fan) | מת על זה! |
| squad number | מספר חולצה (not "מספר סגל") |
| quadruple / treble / double | רביעייה / טרבל / דאבל |
| relegation favourite | מועמדת לירידה |
| N-horse race | מאבק של N קבוצות |
| FFP | מגבלת ההגינות הפיננסית |
| Elsewhere, (transfer round-up) | בינתיים, (results round-up: במגרשים האחרים,) |
| loan in / sign on loan | לקבל בהשאלה (להשאיל = lend out) |
| make X a target | לסמן את X כיעד |
| link X with Y (press) | מקשרים את X ל-Y |
| are believed to be | לפי ההערכות, ... |
| prove costly | לעלות ביוקר |
| turn the team's form around | להחזיר את הקבוצה לכושר |
| get a contract off the books | להיפטר מהחוזה |
| move away from (a formation) | לוותר על |
| played outside the agreed position (loan) | מציבים אותו מחוץ לעמדה שהוסכמה |
| like night and day | הבדל של שמיים וארץ |
| transform the team's fortunes | לחולל מהפך |
| ineligible to sign | אינו רשאי לחתום |
| nervous (fan) | לחוץ (not "עצבני" = angry) |
| take a bow | מגיעות לך מחיאות כפיים |
| Booking points | נקודות משמעת |
| Season Ending Injury List | רשימת פציעות סוף העונה |
| wonderkid | כישרון הפלא |
| the grass is not always greener | הדשא בצד השני לא תמיד ירוק יותר |
| long throw | חוץ ארוך |
| takeover | רכישת השליטה |
| under manager X (unsplit) | תחת ההדרכה של X |
| sign a player (verb) | להחתים (not "לחתום אותו") |
| the grass is greener elsewhere | הדשא של השכן ירוק יותר |
| put the ball in his court | הכדור עכשיו במגרש שלו |
| run down one's contract | לתת לחוזה לפוג |
| come back to haunt us (loan) | יהפוך לבומרנג נגדנו |
| go away and have a think | לשבת ולחשוב |
| I can see where he's coming from | העמדה שלו מובנת לי |
| that wasn't the case this time | אבל לא הפעם |
| prise away | לחלץ |
| bring offers to the table (agent) | להשיג הצעות |
| an easy win (training advice) | שיפור קל להשגה |
| the stuff dreams are made of | חלום שהתגשם |
| late developer (unsplit) | פריחה מאוחרת |
| move forward with (a player) | להמר על |
| just saying (player) | רק שתדעו |
| the intermediary (unsplit) | הגורם המתווך |
| overall | באופן כללי (not "בכלל") |
| [comp] announced | ב-[%comp] הודיעו (a comp takes no gendered verb) |
| leaves the game as (retirement) | נפרד מהמגרשים כ- |
| all-time leader in caps and goals | שיאן ההופעות והשערים של הנבחרת בכל הזמנים |
| cost the team the game | עלה לקבוצה בהפסד |
| consider himself lucky | יכול לברך על מזלו |
| Shows what I know | מה אני מבין בכלל |
| a debut to remember | בכורה בלתי נשכחת |
| make an impact (newcomer) | להשאיר חותם |
| fondly remembered | ייזכר בחיבה |
| do a job on (opponent) | לסדר את |
| former favourite [%person#N] (unsplit) | [%person#N], מהשמות האהובים בעבר ב-X |
| it was all uphill from there | מאותו רגע הכול נהיה קשה |
| turn things around | לשנות את המגמה / להפוך את הקערה על פיה |
| dip my toes into the water (market) | לגשש בשוק בזהירות |
| run X (that) close | לתת ל-X פייט צמוד |
| I consider myself right for the job | אני האדם הנכון לתפקיד |
| believe in my ability | יש לי ביטחון ביכולת שלי |
| take momentum from that game into this | להגיע למשחק הזה עם המומנטום מהקודם |
| stick to the game plan | להיצמד לתוכנית המשחק |
| get distracted | לאבד ריכוז |
| on a massive high | בעננים |
| when it mattered most | כשזה היה הכי חשוב |
| game in hand | משחק חסר |
| vicious circle | מעגל קסמים |
| set the record straight | להעמיד דברים על דיוקם |
| a change is as good as a rest | משנה מקום משנה מזל |
| (injury) is out with X | בחוץ בעקבות X (not "בחוץ עם") |
| a weight off his shoulders | אבן שירדה לו מהלב |
| heart is elsewhere | ליבו כבר במקום אחר |
| broke ranks | יצא נגד הקו הרשמי |
| have one's head turned | היה מתפתה |
| criticism will inspire him | הביקורת תדרבן אותו |
| stretching back to his time at X | עוד מהתקופה שלו ב-X |
| doesn't have the bottle | חסר אומץ |
| the title / relegation picture | תמונת התואר / הירידה |
| cup draw | הגרלת [%comp#1-short] (no ה-) |
| on the sidelines (injured) | מחוץ למגרשים |
| force the issue | להפעיל לחץ |
| another goalscoring appearance | כשכבש שוב |
| push an opponent all the way | להילחם ראש בראש עד הסוף |
| there is a growing belief that | מתחזקת ההערכה ש |
| tempt fate | להתגרות בגורל |
| play down (chances) | להנמיך את הציפיות מ- |
| a leopard can't change its spots | הנמר לא משנה את חברבורותיו |
| begrudgingly gave credit | נתן קרדיט, גם אם בחצי פה |
| home nations (UK) | נבחרות הממלכה המאוחדת |
| X convinced him | X שכנע אותו (not "הוא שוכנע מ-X") |
| throw toys out of the pram | להתנהג כמו ילד מפונק |
| clear the air | ללבן את הדברים |
| can't see it happening | לא נראה לי שזה יקרה |
| buzzing (fan) | בהיי |
| beyond a joke | זה כבר לא מצחיק |
| just pips his teammates | גובר בהפרש זעום על חבריו |
| yo-yoing between divisions | שנים של עליות וירידות |
| step down from playing too | לתלות גם את הנעליים |
| looking elsewhere (player) | מחפש מועדון אחר |
| non-playing role | תפקיד מחוץ למגרש |
| take with a pinch of salt | לקחת בעירבון מוגבל (not "בקורט של מלח") |
| sour grapes | ענבים חמוצים |
| mind games | משחקי ראש |
| backfire | חזר כבומרנג |
| fellow professional | עמית למקצוע |
| I'm afraid (first person) | לצערי |
| ruled out (for N weeks / the season) | ייעדר / יחמיץ את המשך העונה (not "נפסל") |
| if he can't make it (fitness) | אם הוא לא יהיה כשיר |
| write one's name into lore | לחרות את שמו בדברי הימים |
| title challenge / title bid | המאבק על התואר / המרוץ לתואר |
| doesn't seem himself | לא נראה במיטבו |
| remain philosophical (fans) | מקבלים את המצב בשלווה |
| freak accident | תאונה משונה |
| faith repaid | האמון משתלם |
| repay the manager | לגמול למאמן |
| rated 'borderline' for (a match) | השתתפותו מוטלת בספק |
| club signs a player | החתימה את X / השלימה את החתמת X (not "חתמה על X"; a player חותם על חוזה) |
| what many believe to be his market value | שווי השוק שלו לדעת רבים |
| sweat over his future | חושש לעתידו |
| the likes of [position] X | שחקנים כמו ה[position] X |
| get on with his career | לקדם את הקריירה שלו |
| launch a major effort to keep | פתחה במאמץ גדול לשמור |
| shipped out (player) | להיפטר ממנו |
| chequered injury record | לא מעט פציעות בעבר |
| would command a fair price | שווה מחיר הוגן אם יימכר |
| desperate to make the move happen | עושה הכול כדי שהמעבר יצא לפועל |
| leaning towards wanting the move | נוטה להסכים למעבר |
| generally interested (in a move) | די מעוניין |
| re-take control of a contract | לקחת בחזרה את השליטה על החוזה |
| bring the deficit under control | להשתלט על הגירעון |
| high profile players | שמות גדולים |
| financial position is perilous | המצב הכלכלי רעוע מאוד |
| influential captain [%person#N] (unsplit) | הקפטן [%person#N], דמות משפיעה בקבוצה |
| return of N goals | מאזן של N שערים |
| continue to be linked with his signature | על רקע הדיווחים שממשיכים לקשר אותה אליו |
| earn oneself a card | ספג כרטיס |
| suffered the agony of (an own goal) | זה היה רגע מייסר: ... |
| live up to the promise he showed | לממש את ההבטחה שגילה |
| the ex-[team] youngster | הצעיר, לשעבר שחקן [team] |
| from [%team_description#N] [team] | מ[%team_description#N] [team] (not "מידי") |
| top earners | בעלי השכר הגבוה ביותר |
| (release clause) now activated | שנכנס לתוקף |
| establish himself as | לבסס את מקומו כ- |
| rain on their parade | לקלקל להם את החגיגה |
| change tack | שינוי כיוון / שינוי גישה |
| title assault | מכוונים לתואר |
| working relationship | שיתוף הפעולה |
| in a (real) rut | תקועים בבוץ |
| out there (on the pitch) | על המגרש (not "שם בחוץ") |
| (comments) vindicated | התבררו כנכונים |
| two wins out of two | שני ניצחונות בשני משחקים |
| that ship has sailed | הרכבת כבר יצאה |
| ring the changes | שינויים רבים בהרכב |
| X is right (unsplit) | הצדק עם X |
| sit up and take notice | להתעורר ולשים לב |
| go on record | להתבטא בפומבי |
| sensationalise | לנפח / לעשות מזה סיפור |
| the longer the season goes on | ככל שהעונה מתקדמת |
| disingenuous (of us) | לא כן מצדנו |
| cup-tied for all X matches | יהיה מנוע מלשחק במשחקי X |
| play continental football | לשחק במפעלים היבשתיים |
| the only path forward | הפתרון היחיד |
| missed training (AWOL) | נעדר מהאימון |
| hire / dispense with agent [%person#N] (unsplit) | שכר את / ויתר על שירותי הייצוג של [%person#N] |
| [%person#1]'s deputy [%person#2] (unsplit) | [%person#2], יד ימינו של [%person#1] |
| will be in touch | ניצור איתך קשר |
| tensions have been running high | המתיחות גבוהה |
| demoted (disciplinary) | הורדה לסגל נמוך יותר |
| sticky patch | תקופה קשה |
| hoodoo | הקללה |
| lay down a marker | להעביר מסר |
| the buck stops with me | האחריות עליי |
| feel-good story | סיפור מרגש |
| cap a display with N goals | לחתום את ההופעה ב-N שערים (not "להחתים") |
| fully deserved his goal | הרוויח את השער שלו ביושר |
| add to his tally | להוסיף עוד שערים |
| a bright moment in defeat | נקודת אור בתוך ההפסד |
| delightful pass / touches | מסירה נהדרת / נגיעות נהדרות |
| miserable display | הופעה עלובה |
| outgrown the club | כבר גדול על המועדון |
| watching from the stands (unsplit) | לעיני X ביציע / בנוכחות X |
| give him a break! (fan) | תרדו ממנו! |
| go through the motions | לשחק על אוטומט |
| hit the ground running | להתחיל בכל הכוח |
| back me or sack me | או שתתמכו בי או שתפטרו אותי |
| clean-sheet run | רצף שערים נקיים |
| bogey referee | שופט מקולל |
| we're a big scalp | כולם רוצים להפיל אותנו |
| form table | טבלת הכושר |
| go down fighting | להילחם עד הנשימה האחרונה |
| lady luck | גברת מזל |
| take a step closer to avoiding relegation | צעד נוסף להישארות בליגה |
| considering a move for (a player) | שוקלת לפעול להחתמת X |
| award shortlist | רשימת המועמדים הסופיים |
| for the agreement to be respected | כדי לעמוד בהסכם |
| provide cover (squad role) | לשמש גיבוי |
| sensationally axed | הודחו בהפתעה גמורה |
| deter interest from other clubs | להרתיע מועדונים אחרים מלהתעניין |
| injury setback | החמרה בפציעה |
| out for [time] (unsplit hidden player) | ההיעדרות צפויה להימשך [time] |
| champagne football | כדורגל נוצץ ומרהיב |
| handbrake on | בלם יד |
| obligation / option to buy | חובת רכישה / אופציית רכישה |
| an impressive N goals | לא פחות מ-N שערים (not "N שערים מרשימים") |
| succumbed to a defeat | ספגה הפסד |
| not one of their finest hours | לא ייזכר כאחד הרגעים היפים שלהם |
| with the match finely poised | כשהמשחק עוד היה פתוח |
| nursed through the game with an injury | שיחק עם פציעה לאורך המשחק |
| should think (fan) | נראה לי ש... |
| give him the benefit of the doubt | לתת לו ליהנות מהספק |
| take it easy (complacent) | לעשות חיים |
| for [team] (scoring record) | במדי [team] (not "מול השער של") |
| sign (club, verb) | להחתים (not "לחתום איתו") |
| little more than a fringe player | לא הרבה יותר משחקן שוליים |
| he'll be no loss (fan) | הוא לא יחסר לנו |
| have come to regret | עכשיו אנחנו מתחרטים |
| came back to haunt them | יגרום להם להצטער על זה |
| would have been a club record fee | שהייתה שוברת את שיא ההעברות של המועדון |
| looks questionable (a departure) | מעוררת סימני שאלה |
| Not a fan (of a deal) | לא מתלהב מ- |
| tbh (fan post) | האמת, ... |
| going to (future) | plain future (not "הולך ל-") |
| to make matters worse | ולמרבה הצרה |
| improve his case for one (work permit) | לשפר את הסיכויים שלו לקבל אותו |
| old hunting ground | המגרש המוכר לו כל כך |
| joint-most successful team in [comp] history | השוותה את שיא הזכיות בתולדות [comp] |
| prefer to play young players | העדפה לשתף שחקנים צעירים |
| playing him (fan) | לתת לו לשחק |
| looks the real deal | נראה כמו שחקן אמיתי |
| hot prospect | כישרון מבטיח |
| midfield conductor | מנהל משחק בקישור |
| the upside to this deal | הרווח האפשרי מהעסקה |
| never looked back | ומשם לא עצרו (not "ובקושי הביטו לאחור") |
| rarely looked back | ומשם כמעט לא מעדו |
| surpass expectations | לעלות על הציפיות (not "לעקוף") |
| lowest position of Nth | נקודת שפל במקום N |
| only to fall short | אך אז נעצרו |
| back up their pre-season credentials | להצדיק את התחזיות שלפני העונה |
| enough credit (points) to stave off relegation | מספיק נקודות בבנק כדי להדוף את איום הירידה |
| jubilant success | הצלחה משמחת |
| picked up momentum | צברו תאוצה |
| favoured rivals | היריבות שנחשבו לפייבוריטיות |
| consistently defied the odds | הפתיעו שוב ושוב |
| X's agent has indicated his client (unsplit agent) | לפי הסוכן של X, הלקוח... |
| papering over the cracks | לטייח את הסדקים |
| set up for a fall | לטמון פח |
| the show must go on | ההצגה חייבת להימשך |
| succumbed to the disappointment of relegation | ירדה בסופו של דבר ליגה, אכזבה ש... |
| pre-season target / ambitions | היעד שהציבה לפני העונה (not "יעד הכנת העונה") |
| a relegation few saw coming | ירידה שמעטים צפו |
| (title push) falter | המאבק על התואר נחלש |
| fall through the trap door | להידרדר לליגה הנמוכה |
| carry this good run into | להמשיך את הרצף הטוב עד |
| make a surprise push for the title | להפוך למתמודדת מפתיעה על התואר |
| celebrate a job well done | להתגאות בעבודה שעשו |
| flattered to deceive | הבטיחה יותר ממה שקיימה |
| write off (chances) | להספיד את הסיכויים |
| enjoyed a run (stats) | הציגו רצף / רשמו עונה (not "נהנו מרצף") |
| volley / curling shot / diving header | וולה / בעיטה מסולסלת / נגיחה בשלונג |
| bicycle / overhead kick | בעיטת מספרת |
| screamer | טיל |
| edge of the area | קצה הרחבה |
| automatic promotion | עלייה ישירה |
| PFA | איגוד השחקנים (PFA) |
| match practice | דקות משחק |
| bemused at X's inclusion of Y | תמהים על ההחלטה של X לזמן את Y |
| no obligation to play the player | אין חובה לשתף את השחקן |
| come through our youth ranks | להשתלב במחלקת הנוער שלנו |
| achieve some form of respectability | לסיים את העונה בכבוד |
| go public with concerns | הביע בפומבי את החששות |
| with the squad soon to be announced | לקראת פרסום הסגל |
| had fallen out with | הסתכסך עם |
| it's a good read | שווה לקרוא |
| fellow relegation candidates | יריבה נוספת במאבק בתחתית |
| after all | אחרי הכול (not "בסך הכול") |
| a child in X (manager bio) | X, הדור הבא במשפחה |
| just as happy to stay | ישמח באותה מידה להישאר |
| considers the promise kept | מבחינתו ההבטחה קוימה |
| best of the rest | הטובה מבין השאר |
| tinkering (tactics) | שינויים תכופים |
| insider (press) | גורם פנימי |
| overlooked (a rule) | לא שמו לב (התעלמו = deliberately) |
| doesn't mind | לא אכפת לו (not "לו לא אכפת") |
| International Specialist (philosophy) | מומחה לכדורגל נבחרות |
| masterclass (in X) | שיעור מאלף (איך ל-X) |
| live long in the memory | ייחרת בזיכרון |
| (he's) a big loss | זו אבדה גדולה |
| play without him | לשחק בלעדיו |
| war of words continues | מלחמת המילים נמשכת |
| appreciates X's best wishes | תודה ל-X על האיחולים |
| leadership role | תפקיד מנהיגותי |
| set for (youth ranks / a move) | בדרך ל- |
| a rethink could be required | ייתכן שנצטרך לחשוב מחדש |
| daunting | מרתיע |
| comfortable favourites | הפייבוריטיות המובהקות |
| conned the officials | עבד על השופטים |
| jump at the chance | לקפוץ על ההזדמנות |
| one person can't win a match | שחקן אחד לא מנצח משחק לבד |
| make adjustments | לעשות התאמות |
| out of the question | בלתי אפשרי (not "מחוץ לכל שאלה") |
| despite their recent (poor) form | למרות הכושר הפחות טוב לאחרונה |
| firmly on the agenda | כבר ממש על הפרק |
| flying start | פתיחה סוערת |
| lightning-fast goal | שער בזק |
| within touching distance of safety | במרחק נגיעה מהמקומות הבטוחים |
| X withdrawn from squad (headline) | X מחוץ לסגל |
| making light of the run-in | עוברים את הישורת האחרונה בקלות |
| bound for something more | בדרך למשהו גדול יותר |
| run away with the title | לברוח עם האליפות |
| hovering close to the drop zone | קרובה באופן מסוכן לאזור הירידה |
| sitting pretty on N points | נמצאת במקום נוח עם N נקודות |
| champions-in-waiting | נראית כמו האלופה הבאה |
| in the title conversation | בתמונת התואר |
| failure to X (bio) | העובדה שלא X / מכיוון שלא הצליחה ל-X |
| propping up the table | המקום האחרון בטבלה |
| feeder club / parent club | מועדון בת / מועדון אם |
| sanction / transfer embargo (FFP) | עיצום / עיצום העברות |
| forced relegation | ירידה כפויה |
| drop the issue | ניתן לעניין לרדת מהפרק |
| average points table | טבלת ממוצע הנקודות |
| don't count your chickens | לא מוכרים את עור הדוב לפני שצדו אותו |
| dead rubber | משחק חסר חשיבות |
| daisy cutter | בעיטה קרקעית |
| take it or leave it offer | הצעה של 'קחו או עזבו' |
| season curtain-raiser / closer | פתיחת העונה / אקורד הסיום של העונה |
| owed an assist to the woodwork | המסגרת בישלה לה |
| continental hangover | ההנגאובר היבשתי |
| tipped / backed / expected to (finish X) | צפו לה X / סומנה כמועמדת ל-X (not "נחזתה ל-") |
| costly results | תוצאות שעלו לה ביוקר |
| turn the script on its head | לטרוף את הקלפים |
| title bid in tatters | ניפצו את המאבק על התואר |
| hanging by a thread | תלויות על חוט השערה |
| arrest the slide | לבלום את ההידרדרות (not "הירידה") |
| litmus test of credentials | מבחן לקמוס ליכולת האמיתית |
| winner-takes-all play-off | פלייאוף של הכול או כלום |
| need no introduction | לא צריכות הצגה |
| make a mockery of the forecasts | להפוך את התחזיות לבדיחה |
| indifferent form | כושר בינוני (not "אדיש") |
| one-two (pass) | משחק קירות |
| channels (runs into) | מסדרונות |
| first-time shot | בעיטת מגע ראשון |
| trial day | יום מבחנים |
| head-to-head (own match) rule | כלל המפגש הישיר |
| solidarity contributions | תשלומי סולידריות |
| dangerman | השחקן המסוכן |
| grudge match | משחק עם חשבון פתוח |
| scrappy win | ניצחון מקרטע |
| national FA | התאחדות הכדורגל של [%nation#N] (no ה- before the token) |
| the stakes couldn't be higher | מה שמונח על הכף לא יכול להיות גדול יותר |
| clean sweep (of honours) | לזכות בכל התארים |
| tournament heavyweight | אחת הגדולות |
| playing hardball | מקשיחה עמדות |
| low-balling us | מציעה לנו פירורים |
| unsettled (player) | לא מרגיש בנוח במועדון |
| facing relegation (prediction) | צפויה לרדת מ- |
| arrival of new manager X (unsplit) | המינוי של X להדרכת הקבוצה |
| showpiece occasion (final) | הגמר |
| inject new life into | להפיח חיים חדשים ב- (not "להנשים") |
| continuity (over upheaval) | המשכיות (not "רצף") |
| have half an eye on | שוקלים (not "שמים חצי עין") |
| the title is theirs to lose | התואר הוא שלה, אלא אם תאבד אותו בעצמה |
| more likely than not (parting) | פרידה היא התרחיש הסביר |
| clear-out (squad) | ניקוי הסגל |
| ease the pressure on the books | להקל על הלחץ על הקופה |
| new regime (owners) | הבעלים החדשים |
| manager [%person#N] (unsplit, standard) | ההדרכה בראשות [%person#N] / מצד [%person#N] על הספסל |
| losing him / replacing him (noun) | אובדנו / החלפתו (not "איבוד אותו") |
| it has been suggested that | נטען ש (not "הוצע ש") |
| it is understood that | לפי המידע, |
| word has reached the media | לתקשורת דלף ש |
| under-performance (board) | תפקוד חלש |
| dips in confidence | משברי אמון |
| goodwill left in the bank | קרדיט |
| found wanting | לא הוכיחה את עצמה |
| out of form / mixed form | בכושר ירוד / בכושר הפכפך |
| domestic-based players | שחקנים מהליגה המקומית (not "מהארץ") |
| the board wanted a manager with X (in a split) | ההנהלה רצתה מישהו עם X |
| [%club#N-short] / [%club_list#N] (grammar) | feminine singular / feminine plural, like team names (מבקשת, מתעניינות) |
| something close to a miracle | כמעט נס |
| separated by the finest of margins | רק פער זעום מפריד בין |
| too close to call | אי אפשר לדעת מי תנצח |
| basking in the glow (of promotion) | מתבשמת מההישג |
| first approach (offer) | ההצעה הראשונית |
| mandatory future fee | תשלום עתידי מחייב |
| hold out (negotiation) | להתעקש |
| bumper crowd | קהל עצום |
| in contrasting form | במצבי כושר מנוגדים |
| recruitment team | צוות הסקאוטינג |
| underperform | לאכזב (not "להתאכזב") |
| at the wrong end of the table | בתחתית הטבלה |
| It sees X (report opener) | בעקבותיו / בעקבות זאת |
| muster a fight for | למצוא כוח להילחם על |
| with games running out | כשנותרו משחקים מעטים |
| knocked out by X | X הדיחה את (not "הודחה על ידי") |
| can't separate (two sides) | אין לי דרך להכריע בין |
| goes down as a draw in my book | מבחינתי זה תיקו |
| lacks grace | אין לו רוח ספורטיבית |
| you're being harsh (on me) | זו ביקורת קשה מדי |
| beat the offside trap | שבירת מלכודת הנבדל |
| will remain in charge (headline) | ממשיכים עם X |
| confident of promotion (headline) | X: נעלה ליגה |
| leave unchecked (checkbox) | אל תסמנו |
| holders (cup) | המחזיקה בתואר |
| Goal-line Technology | טכנולוגיית קו השער |
| Video Assistant Referee | עוזר השופט לווידאו (VAR) |
| Marquee Player (squad status) | שחקן כוכב |
| board mood: delighted / very pleased / pleased / satisfied | מאושרת / מרוצה מאוד / מרוצה / שבעת רצון |
| [comp] proper | השלב הראשי של [comp] |
| latter stages | השלבים המתקדמים |
| Newgen | שחקן שנוצר במשחק; Nation Newgen Specifications = הגדרות שחקנים מחוללים לפי מדינה (UI) |
| Technical Director | מנהל טכני |
| Non-Nation Born | יליד חו״ל |
| team fluidity | גמישות קבוצתית (קשיחה מאוד / קשיחה / מאוזנת / גמישה / גמישה מאוד) |
| team mentality | גישת הקבוצה |
| added/removed team instruction | נוספה/הוסרה הוראה קבוצתית: ... |
| tactical roles (descriptions) | Anchor = עוגן; Deep-Lying Playmaker = פליימייקר אחורי; Ball-Winning Midfielder = קשר חוטף כדורים; Complete Forward = חלוץ שלם; Deep-Lying Forward = חלוץ נסוג; Poacher = חלוץ רחבה; Target Forward = חלוץ מטרה; Water Carrier = נושא המים; Segundo Volante = סגונדו וולאנטה |
| clear-cut chances | מצבים ודאיים |
| coaching badge | הסמכת אימון |
| negative body language | שפת גוף שלילית |
| removed instruction for X (backroom) | הוסרה ההוראה ל-[%person#1]: <UI label> |
| started training X (trait) | החל אימון עבור [%person#1-surname]: <noun phrase> |
| interim / caretaker manager | מאמן זמני |
| final third / opposition box | השליש האחרון / רחבת היריבה |
| conversion rate | אחוז הניצול |
| coaching staff / medical staff | צוות המאמנים / הצוות הרפואי |
| Hall of Fame | היכל התהילה |
| mentoring group | קבוצת חונכות |
| recruitment focus | מוקד גיוס |
| captaincy should go to X | הקפטנות צריכה להיות של X |
| squad statuses (UI) | שחקן כוכב / שחקן חשוב / פותח קבוע / שחקן סגל / מחליף משנה משחק / שוער ראשון / שוער גביע / שחקן שוליים / כישרון חם / כישרון פורץ |
| supporter types: Hardcore / Corporate / Casual | אדוקים / עסקיים / נינוחים |
| Chief Scout | הסקאוט הראשי |
| Informational Objectives | יעדים לידיעה |
| I can see where you're coming from | העמדה שלכם מובנת לי (not "ברור לי מאיפה אתם באים") |
| cooling-off period | תקופת צינון |
| beside themselves with anger | רותחים מזעם (not "יוצאים מגדרם") |
| be around for a while (stay) | להישאר לאורך זמן (not "זמן מה") |
| show glimpses of (promise) | יש פה ושם סימנים מעניינים |
| there is recognition that | מכירים בכך ש |
| not on board with (adopting X) | לא מוכנים לאמץ X |
| the fixture pairs X with Y | המשחק מפגיש את X עם Y |
| hard-fought clash | מפגש קשוח |
| ahead of schedule | מוקדם מהמתוכנן |
| recent defensive record | המאזן ההגנתי לאחרונה |
| recent home form | משחקי הבית האחרונים |
| do things your way | לעשות את זה בדרך שלכם |
| through good times and bad | בטוב וברע |
| question (a run of results) | לתהות על |
| unable to start (training a move) | לא ניתן להתחיל לאמן את X ב- |
| What can I do for you? (to staff) | במה אוכל לעזור? |
| you're the boss | אתם הבוסים |
| set up for failure | דאגתם שאכשל |
| feel cheated | יש לי תחושה שעבדו עליי |
| my client (unsplit agent) | הצד שאני מייצג |
| buy-in (squad) | מחויבות |
| team meeting | ישיבת קבוצה |
| set-piece routine | תרגיל |
| in/out-swinging cross | הגבהה מסובבת פנימה / החוצה |
| near / far post | קורה קרובה / רחוקה |
| buy-in levels | נלהבים / מעורבים / מאמינים / מסורים |
| chip / lob / half-volley | צ'יפ / לוב / חצי וולה |
| first time / one touch | במגע ראשון / במגע אחד |
| into the path of X | אל נתיב הריצה של X |
| dive / simulation | צלילה / הצגה |
| headbutt | מכת ראש (not "הנחת ראש") |
| mindset(s) | הלך רוח / הלכי רוח |
| byline | קו הסיום |
| scrambled clearance | הרחקה בחיפזון |
| pot-shot | בעיטה לא מחושבת |
| piledriver | פצצה |
| looping header | נגיחה קשתית |
| marching orders | הוראה לעזוב את המגרש |
| off his line (keeper) | מחוץ לקו השער |
| brace (two goals) | צמד |
| loose ball / rebound | הכדור החופשי / הכדור החוזר |
| let-off | מזל גדול |
| hit the bar | פגיעה במשקוף |
| trademark (finish) | סימן ההיכר |
| run down the clock at the corner flag | ליד דגל הקרן, שורף את השעון |
| through ball | כדור עומק |
| backpass | מסירה אחורה |
| looks for / searches out X (unsplit) | [%person#1] מנסה למצוא את X |
| moves the ball to the left | הכדור עובר שמאלה דרך X |
| It would have been a great goal | זה היה יכול להיות שער נהדר |
| looks for the head of X | כדור אל הראש של X |
| went down looking for a decision | נפילה בניסיון לסחוט שריקה |
| suggestions of simulation | חשד להצגה |
| back post | הקורה הרחוקה |
| The injured X is replaced by Y | החלפה בגלל פציעה: X החוצה, Y פנימה |
| run off an injury | להמשיך לשחק למרות הפציעה |
| with the goal at his mercy | מול שער פתוח |
| has his name taken (booked) | נרשם בפנקס של השופט |
| on thin ice (one card from a red) | על חבל דק |
| wants the ground to open up | רוצה שהאדמה תבלע אותו |
| puts it into orbit | נשלחת לחלל |
| hopeful shot | בעיטה אופטימית |
| It's there! / That's in! | בפנים! |
| looks for X to run onto it (unsplit) | מסירה אל הריצה של X |
| goes close (unsplit X) | ניסיון קרוב של X (not "X קרוב!") |
| live commentary passives | short noun lines ("חטיפה יפה של X", "בעיטה חופשית של X"), not "על ידי X" |
| role model | מודל לחיקוי |
| hold my hands up | אני לא מתכחש: ... |
| non-playing staff | הצוות המקצועי |
| forced out (player) | דוחקים אותי החוצה |
| beat X to the ball (unsplit) | ניצחון של X על Y במרוץ לכדור |
| hold off (an opponent) | להדוף בגוף / עבודת גוף (not "הרחקה") |
| shrug off the attentions of | השתחררות מהצמדה של |
| spots the run of (unsplit) | עין טובה של X לריצה של Y |
| has the legs on | יתרון מהירות על |
| fire in his belly | אש בעיניים |
| not himself | לא נראה כמו עצמו |
| service (to a striker) | הכדורים שמגיעים ל-X |
| from all of N yards | ממרחק של לא פחות מ-N יארד |
| leaves Y standing | עקיפה של X שמשאירה את Y במקום |
| whistle (object) | משרוקית |
| what was the point? | מה הטעם? |
| didn't play me | לא שיתפתם אותי (not "שיחקתם אותי") |
| sold me a dream | מכרתם לי אשליות |
| takes it in his stride (ball) | קולט את הכדור בתנועה |
| latches onto the ball | התלבשות של X על הכדור |
| gives the ball away (live) | מתנה ליריב מ-X |
| X surely! (about to score) | X, זה חייב להיות גול! |
| takes on X (dribble) | X מול Y, אחד על אחד (not "דו-קרב") |
| beaten all ends up | ל-Y לא היה שום מענה ל-X |
| nutmeg | לשחיל את הכדור בין הרגליים של X |
| come on you lot | יאללה חבר'ה |
| formality | עניין של מה בכך |
| kick on | להמשיך מכאן |
| show a good account of yourselves | לצאת בכבוד |
| heads down | להתרכז בעבודה |
| their manager (unsplit, commentary) | על הספסל שלהם / השיחה בהפסקה (not "המאמן שלהם") |
| really got his foot in there | שם רגל חזקה |
| coughs up the ball (keeper) | איזו מתנה של X! |
| will want that one back (keeper) | ל-X בטח יש חרטה על השער הזה |
| announces his arrival | מציג את עצמו לעולם |
| for what it's worth | לידיעתכם, |
| experienced heads | שחקנים מנוסים |
| one last hurrah | סיבוב אחד אחרון |
| is set to be confirmed as (new manager) | צפויה לאשר את מינוי X |
| insiders | יודעי דבר (not "גורמים פנימיים") |
| it was even (across the pitch) | היה שוויון (not "המצב היה שווה") |
| well-established within the squad | בעל מעמד מבוסס בסגל / עדיין לא ביסס את מעמדו |
| unhappiness (player) | חוסר שביעות רצון (not "חוסר אושר") |

## Job and position nouns (in-game test 2026-11-26)

FM prints only the base key's text, for men and women alike; no -F variant of a job or position is ever shown. Job titles, position names and role names must therefore read correctly for both genders:
- In labels and lists use the noun as a title (מאמן ראשי, עוזר מאמן, שוער, חלוץ). These read as titles, not as describing a gendered person.
- In sentences about a person, avoid gender agreement with the job: write "בתפקיד [%job#1]" / "בעמדת [%position#1]" rather than an adjective or verb that agrees with the noun.
- Never add a feminine form (מאמנת, שוערת) in a base key text.

| Outlet roles (UI) | Direct Outlet = מוצא ישיר; Wide Outlet = מוצא אגפי; Central Outlet = מוצא מרכזי; Splitting Outlet = מוצא מפצל; Inverting/Inside Outlet = מוצא פנימי (never כתובת) |

## Reserve teams (decision 2026-11-26, project lead)
| English | Hebrew |
|---|---|
| Reserve team / squad / league | קבוצת המילואים / סגל המילואים / ליגת המילואים; club reserve sides "X מילואים" or "X ב'" per the club-name pattern; short fields may use מיל' |
| NOT used | רזרבות / רזרבה for teams (רזרבה only for financial reserves; a backup player is שחקן ספסל), and עתודה only where the UI already uses it for youth/academy |
