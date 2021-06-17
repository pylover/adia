import re
from collections import namedtuple


EOF = 0
NAME = 1
NL = 2
AT = 3
DOT = 4
COLON = 5
LPAR = 6
RPAR = 7
COMA = 8
RARROW = 9
INDENT = 10
DEDENT = 11
BACKSLASH = 12


EXACT_TOKENS = [
    ('->',  2, RARROW),
    ('@',   1, AT),
    ('.',   1, DOT),
    (':',   1, COLON),
    ('(',   1, LPAR),
    (')',   1, RPAR),
    (',',   1, COMA),
    ('\\',  1, BACKSLASH),
    ('\n',  1, NL),
]


# Regex patterns
WHITESPACE_RE = r'\s+'
NAME_RE = r'\w+'
ALLTOKENS_RE = \
    [re.escape(i[0]) for i in EXACT_TOKENS] + [WHITESPACE_RE, NAME_RE]
ALLTOKENS_RE = re.compile('(' + '|'.join(ALLTOKENS_RE) + ')')
TOKENS_DICT = {t: n for t, _, n in EXACT_TOKENS}

# Token namedtuple
Token = namedtuple('Token', 'type string start end line')


def EOFToken(lineno, line):
    return Token(EOF, '', (lineno, 0), (lineno, 0), '')


def IndentToken(lineno, token, start, end, line):
    return Token(INDENT, token, (lineno, start), (lineno, end), line)


def DedentToken(lineno, lineindent, indentsize, line):
    return Token(
        DEDENT, '',
        (lineno, lineindent * indentsize),
        (lineno, lineindent * indentsize),
        line
    )


def tokenize(readline):
    lineno = 0
    indentsize = 0
    indent = 0
    escape = False
    newline = True

    while True:
        line = readline()
        lineno += 1

        if line == '':
            yield EOFToken(lineno, line)
            break

        for m in ALLTOKENS_RE.finditer(line):
            token = m.group()
            start, end = m.span()

            if newline and (start == 0):  # Beginning of line
                lineindent = 0
                if token.startswith(' '):  # Whitespace
                    # Indentation
                    if not indentsize:
                        indentsize = end - start

                    lineindent = (end - start) // indentsize

                if lineindent > indent:
                    indent = lineindent
                    yield IndentToken(lineno, token, start, end, line)

                elif lineindent < indent:
                    for i in range(indent - lineindent):
                        indent -= 1
                        yield DedentToken(lineno, lineindent, indentsize, line)

            if token.startswith(' '):  # Whitespace
                # Ignore for the now.
                continue

            if token == '\\':  # Escape
                escape = True
                continue

            if escape:
                escape = False
                continue

            newline = token == '\n'
            yield Token(
                TOKENS_DICT.get(token, NAME),
                token,
                (lineno, start),
                (lineno, end),
                line
            )
