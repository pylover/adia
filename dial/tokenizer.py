import re

from .token import *

# Regex patterns
WHITESPACE_RE = r'\s+'
NAME_RE = r'\w+'
ALLTOKENS_RE = \
    [re.escape(i[0]) for i in EXACT_TOKENS] + [WHITESPACE_RE, NAME_RE]
ALLTOKENS_RE = re.compile('(' + '|'.join(ALLTOKENS_RE) + ')')
TOKENS_DICT = {t: n for t, _, n in EXACT_TOKENS}


def EOFToken(lineno, line):
    return Token(EOF, '', (lineno, 0), (lineno, 0), '')


def IndentToken(lineno, token, coloffset, start, end, line):
    start += coloffset
    return Token(INDENT, token[coloffset:], (lineno, start), (lineno, end),
                 line)


def DedentToken(lineno, coloffset, lineindent, indentsize, line):
    return Token(
        DEDENT, '',
        (lineno, lineindent * indentsize + coloffset),
        (lineno, lineindent * indentsize + coloffset),
        line
    )


def NewlineToken(lineno, token, start, end, line):
    return Token(NL, token, (lineno, start), (lineno, end), line)


def tokenize(readline):
    lineno = 0
    coloffset = -1
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

            if token == '\\':  # Escape
                escape = True
                continue

            if escape:
                escape = False
                continue

            if newline and (start == 0):  # Beginning of line
                lineindent = 0
                if token.startswith(' '):  # Whitespace
                    # Indentation
                    if coloffset < 0:
                        coloffset = end

                    elif not indentsize:
                        indentsize = end - coloffset

                    if indentsize:
                        lineindent = (end - coloffset) // indentsize

                elif token not in ['\n'] and coloffset < 0:
                    coloffset = start

                if lineindent > indent:
                    indent = lineindent
                    yield IndentToken(lineno, token, coloffset, start, end,
                                      line)

                elif lineindent < indent:
                    for i in range(indent - lineindent):
                        indent -= 1
                        yield DedentToken(lineno, coloffset, lineindent,
                                          indentsize, line)

            if token.startswith(' '):  # Whitespace
                # Ignore for the now.
                continue

            newline = token == '\n'
            if newline:
                yield NewlineToken(lineno, token, start, end, line)
                continue

            yield Token(
                TOKENS_DICT.get(token, NAME),
                token,
                (lineno, start),
                (lineno, end),
                line
            )
