import re
from collections import namedtuple


EOF = 0
NAME = 1
NL = 2
AT = 3
COLON = 4


EXACT_TOKENS = [
    ('@',  1, AT),
    (':',  1, COLON),
    ('\n', 1, NL),
]


WHITESPACE = r'\s+'
NAME = r'\w+'
ALLTOKENS = [i[0] for i in EXACT_TOKENS] + [WHITESPACE, NAME]
TOKENS_DICT = {t: n for t, _, n in EXACT_TOKENS}
ALLTOKENS_RE = re.compile('(' + '|'.join(ALLTOKENS) + ')')


Token = namedtuple('Token', 'type string start end line')


def tokenize(readline):
    lineno = 0

    while True:
        line = readline()
        lineno += 1

        if line == '':
            yield Token(EOF, line, (lineno, 0), (lineno, 0), line)
            break

        for m in ALLTOKENS_RE.finditer(line):
            token = m.group()
            span = m.span()

            if token.startswith(' '):
                # Just ignore for now
                continue

            yield Token(
                TOKENS_DICT.get(token, NAME),
                token,
                (lineno, span[0]),
                (lineno, span[1]),
                line
            )
