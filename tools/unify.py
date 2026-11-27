"""One form for recurring terms that translation batches wrote differently (glossary.md decides).

    python tools/unify.py [prefix]        rewrites work/done/<prefix>*.json in place, prints counts

Only unambiguous phrases are replaced (e.g. not a bare "עקיפה", which can also mean an indirect kick).
"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES = [
    ('מועדון מסונף', 'מועדון שותף'),
    ('מועדון קשור', 'מועדון שותף'),
    ('שחקן ייעודי', 'שחקן מיועד'),
    ('בסיכום שני המשחקים', 'בתוצאה המצטברת'),
    ('העפלה למפעל אירופי', 'העפלה למפעל יבשתי'),
    ('העפלה ליבשתית', 'העפלה למפעל יבשתי'),
    ('עקיפה מבפנים', 'חפיפה פנימית'),
    ('עקיפה פנימית', 'חפיפה פנימית'),
    ('עקיפה מבחוץ', 'חפיפה'),
    ('עקיפה (מבחוץ)', 'חפיפה'),
    ('שינוי טקטי', 'כוונון טקטי'),
    ('שינויים טקטיים', 'כוונונים טקטיים'),
    ('הירתמות', 'מחויבות'),
    ('אמון בחזון', 'מחויבות'),
    ('שוטאאוט', 'דו-קרב פנדלים'),
    ('רשימה קצרה', 'רשימת מעקב'),
    ('זכות ההתרברבות', 'הכבוד בעיר'),
    ('זכויות התפארות', 'הכבוד בעיר'),
    ('בהזכות להתגאות', 'בכבוד בעיר'),
    ('להזכות להתגאות', 'לכבוד בעיר'),
    ('בהכבוד בעיר', 'בכבוד בעיר'),
    ('להכבוד בעיר', 'לכבוד בעיר'),
    ('ביום המחזור האחרון', 'במחזור האחרון'),
    ('מעט גבות עלו', 'כמעט איש לא הופתע'),
    ('משחקי ההישרדות', 'פלייאוף הירידה'),
    ('יחס השערים', 'הפרש השערים'),
    ('לחפש עקיפה', 'לחפש חפיפה'),
    ('רשימת הנכים', 'רשימת הפצועים'),
    ('דראפט החזרה', 'דראפט הכניסה מחדש'),
    ('דראפט הכניסה המחודשת', 'דראפט הכניסה מחדש'),
    ('ה-VAR היה גורם', 'ה-VAR מילא תפקיד'),
    ('VAR היה גורם', 'ה-VAR מילא תפקיד'),
    ('ה-ה-VAR', 'ה-VAR'),
    ('ניצוץ של תקווה', 'זיק של תקווה'),
    ('קונטיננטלי פרו', 'פרו יבשתי'),
    ('קונטיננטלי A', 'A יבשתי'),
    ('קונטיננטלי B', 'B יבשתי'),
    ('קונטיננטלי C', 'C יבשתי'),
    ('קונטיננטל פרו', 'פרו יבשתי'),
    ('קונטיננטל A', 'A יבשתי'),
    ('קונטיננטל B', 'B יבשתי'),
    ('חיפוש עקיפה', 'חיפוש חפיפה'),
    ('דראפט הווייבר', 'דראפט הוויתורים'),
    ('רשימת הווייבר', 'רשימת הוויתורים'),
    ('לווייבר', 'לוויתורים'),
    ('קרן הקצאה כללית', 'כספי הקצאה כללית'),
    ('קרן ההקצאה הכללית', 'כספי ההקצאה הכללית'),
    ('חשבון השכר', 'הוצאות השכר'),
    ('הסיוע בשכר', 'ההשתתפות בשכר'),
    ('כדורגל משעשע', 'כדורגל מהנה'),
    ('מספרי סגל', 'מספרי חולצות'),
    ('מספר סגל', 'מספר חולצה'),
    ('ברכה בתחפושת', 'ברכה במסווה'),
    ('הורמו גבות', 'עורר פליאה'),
    ('בקורט של מלח', 'בעירבון מוגבל'),
    ('ביום [%date#', 'ב-[%date#'),
    ('שם בחוץ', 'על המגרש'),
    ('ללחום', 'להילחם'),
    ('מה הייתה הנקודה', 'מה הטעם'),
    ('מכרתם לי חלום באצבע', 'מכרתם לי אשליות'),
    ('הנחת ראש', 'מכת ראש'),
    ('הקורה האחורית', 'הקורה הרחוקה'),
    ('שוער ספסל', 'שוער גיבוי'),
    ('ברור לי מאיפה אתם באים', 'העמדה שלכם מובנת לי'),
    ('תנשים חיים חדשים', 'תפיח חיים חדשים'),
    ('להנשים חיים חדשים', 'להפיח חיים חדשים'),
    ('על מה שרבים מאמינים שהוא שווי השוק שלו', 'על שווי השוק שלו לדעת רבים'),
    ('על מה שרבים מאמינים שהוא שווי השוק שלה', 'על שווי השוק שלה לדעת רבים'),
    ('הכדורגל ה-[%nation#1-nationality]', 'הכדורגל של [%nation#1]'),
    ('הכדורגל ה-[%nation#2-nationality]', 'הכדורגל של [%nation#2]'),
    ('בלי אותו', 'בלעדיו'),
    ('בלי אותה', 'בלעדיה'),
    ('עבור אותו', 'עבורו'),
    ('עבור אותה', 'עבורה'),
    ('מחוץ לכל שאלה', 'בלתי אפשרי'),
    ('עקפו את הציפיות', 'עלו על הציפיות'),
    ('עקפה את הציפיות', 'עלתה על הציפיות'),
    ('ובקושי הביטו לאחור', 'ומשם כמעט לא מעדו'),
    ('תחת המאמן החדש [%person#', 'תחת ההדרכה החדשה של [%person#'),
    ('מערכת היחסים העובדת', 'שיתוף הפעולה'),
    ('לוויברים', 'לוויתורים'),
    ('הוויברים', 'הוויתורים'),
    ('מהוויברס', 'מרשימת הוויתורים'),
    ('הליך הוויברס', 'הליך הוויתורים'),
    ('בבחירה הבאה בווייבר', 'בבחירה הבאה ברשימת הוויתורים'),
    ('בבקשת הווייבר', 'בבקשת הוויתורים'),
    # Outlet roles: the UI (carried) says Direct Outlet = מוצא ישיר
    ('כתובת אגפית', 'מוצא אגפי'),
    ('כתובת מרכזית', 'מוצא מרכזי'),
    ('כתובת מפצלת', 'מוצא מפצל'),
    ('כתובת פנימית', 'מוצא פנימי'),
    # backup player = שחקן ספסל (רזרבה only for financial reserves)
    ('כשחקן רזרבה', 'כשחקן ספסל'),
    ('שחקן רזרבה', 'שחקן ספסל'),
    ('כרזרבה', 'כשחקן ספסל'),
    ('עבור רזרבה', 'עבור שחקן ספסל'),
    ('אופציית רזרבה', 'אופציה לספסל'),
    ('הכתובת המפצלת', 'המוצא המפצל'),
    ('הכתובת הפנימית', 'המוצא הפנימי'),
    ('הכתובת האגפית', 'המוצא האגפי'),
    ('הכתובת המרכזית', 'המוצא המרכזי'),
]


import re
OWN = r'(job|position|tactical_role|injury|foul|basic_goal_description|conditions_description)'
PREFIX_RX = re.compile(r'(?<![א-ת])([ו]?[בהלמשכ]|[ו])-(\[%' + OWN + r'#)')


# no ה- before a name token (the glossary): "במשחק ה-[%comp" -> "במשחק [%comp", "מה-[%comp" -> "מ-[%comp"
NAME_H = re.compile(r'(?<![א-ת])([ומשבלכ]?)ה-(\[%(?:comp|award|fixture_name|team|club|stadium|city)#)')


SIGNED = re.compile(r'(?<![א-ת])([ושכ]?)ה*חתמנו אות(?=[וה])')
SIGNED_OK = 'החתמנו אות'


def fix(v, counts):
    if isinstance(v, dict):
        return {k: fix(x, counts) for k, x in v.items()}
    if not isinstance(v, str):
        return v
    # club signs a player: "(ש)חתמנו אותו" -> "(ש)החתמנו אותו" (never touch an existing החתמנו)
    w = SIGNED.sub(lambda m: m.group(1) + SIGNED_OK, v)
    if w != v:
        counts['signed'] = counts.get('signed', 0) + 1
        v = w
    k = len(NAME_H.findall(v))
    if k:
        counts['name-h'] = counts.get('name-h', 0) + k
        v = NAME_H.sub(lambda m: (m.group(1) + '-' if m.group(1) else '') + m.group(2), v)
    n = len(PREFIX_RX.findall(v))
    if n:
        counts['prefix-'] = counts.get('prefix-', 0) + n
        v = PREFIX_RX.sub(lambda m: m.group(1) + m.group(2), v)
    for a, b in RULES:
        if a in v:
            counts[a] = counts.get(a, 0) + v.count(a)
            v = v.replace(a, b)
    return v


# "Elsewhere," is "במגרשים האחרים," only in results; in transfer round-ups it is "בינתיים,".
TRANSFER = re.compile(r'transfer|loan|sign|bid|deal|offer|interest|link|target|move|contract|fee|scout|rumou?r', re.I)


def elsewhere(en, v, counts):
    if isinstance(v, dict):
        return {k: elsewhere(en, x, counts) for k, x in v.items()}
    if not isinstance(v, str) or 'Elsewhere' not in en:
        return v
    a, b = ('במגרשים האחרים,', 'בינתיים,') if TRANSFER.search(en) else ('במקום אחר,', 'במגרשים האחרים,')
    if a in v:
        counts[a + ' -> ' + b] = counts.get(a + ' -> ' + b, 0) + 1
        v = v.replace(a, b)
    return v


def main():
    pre = sys.argv[1] if len(sys.argv) > 1 else ''
    counts = {}
    units = json.load(open(os.path.join(ROOT, 'work', 'en', 'units.json'), encoding='utf-8'))
    for p in sorted(glob.glob(os.path.join(ROOT, 'work', 'done', pre + '*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        new = {k: elsewhere(units[int(k)]['en'], fix(v, counts), counts) for k, v in d.items()}
        if new != d:
            json.dump(new, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    if counts.get('signed'):
        print(f"{counts['signed']:5} signing verb fixed (החתמנו)")
    if counts.get('name-h'):
        print(f"{counts['name-h']:5} ה- removed before name tokens (comp, award...)")
    if counts.get('prefix-'):
        print(f"{counts['prefix-']:5} hyphen removed before own-Hebrew tokens (job, position...)")
    for a, b in RULES:
        if counts.get(a):
            print(f'{counts[a]:5} {a} -> {b}')
    for k, n in counts.items():
        if ' -> ' in k:
            print(f'{n:5} {k} (Elsewhere)')


if __name__ == '__main__':
    main()
