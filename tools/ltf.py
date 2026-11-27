"""Read and write Football Manager custom language text files (.ltf).

FM writes a template, Documents\\Sports Interactive\\Football Manager 27\\languages\\example.ltf:
    # comment
    LANGNAME: <name shown in Preferences>
    GENDERS: 0
    BASESTRINGS: 0

    KEY-<id>: <English text, possibly over several lines>[COMMENT ...]
    STR-1: <translation>
    KEY-<id>-M: <male variant>          (gender variants of the same id follow directly)
    STR-1:
    KEY-<id>-F: <female variant>
    STR-1:

A line starting with "KEY-<id>[-M|-F]: " starts an entry, "STR-<n>: " its translation; other lines
continue the text before them. Empty STR-1 falls back to English.
"""
import re

KEY = re.compile(r'^KEY-(\d+(?:-[A-Z]+)?): ?(.*)$')
STR = re.compile(r'^STR-(\d+): ?(.*)$')
COMMENT = re.compile(r'\[COMMENT[^\]]*\]', re.S)


def read(path):
    """Returns (header lines, [(key, english with comments)]) in file order."""
    lines = open(path, encoding='utf-8-sig').read().split('\n')
    head, entries, cur, mode = [], [], None, None
    for line in lines:
        m = KEY.match(line)
        if m:
            cur = [m.group(1), m.group(2)]
            entries.append(cur)
            mode = 'key'
            continue
        if STR.match(line):
            mode = 'str'
            continue
        if cur is None:
            head.append(line)
        elif mode == 'key':
            cur[1] += '\n' + line
    for e in entries:
        e[1] = e[1].rstrip('\n')
    return head, [tuple(e) for e in entries]


def plain(en):
    """English text without [COMMENT ...] notes."""
    return COMMENT.sub('', en).strip()


def write(path, langname, entries, translations, genders=0):
    """entries from read(); translations {key: Hebrew}. Missing keys get an empty STR-1."""
    with open(path, 'w', encoding='utf-8-sig', newline='\n') as f:
        f.write('# Language Text File Generated for Football Manager\n')
        f.write(f'LANGNAME: {langname}\nGENDERS: {genders}\nBASESTRINGS: 0\n\n')
        for key, en in entries:
            f.write(f'KEY-{key}: {en}\nSTR-1: {translations.get(key, "")}\n')
