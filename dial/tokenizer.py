import io
import re

from .token import *

# Regex patterns
WHITESPACE_RE = r' +'
NAME_RE = r'\w+'
NEWLINE_RE = re.escape('\n')
ALLTOKENS_RE = \
    [re.escape(i[0]) for i in EXACT_TOKENS] + \
    [WHITESPACE_RE, NAME_RE, NEWLINE_RE]
ALLTOKENS_RE = re.compile('(' + '|'.join(ALLTOKENS_RE) + ')')
TOKENS_DICT = {t: n for t, n in EXACT_TOKENS}


class Tokenizer:
    def __init__(self):
        self.lineno = 0
        self.coloffset = -1
        self.indentsize = 0
        self.indent = 0
        self.escape = False
        self.newline = True

    def _eoftoken(self, line):
        return Token(EOF, '', (self.lineno, 0), (self.lineno, 0), '')

    def _indenttoken(self, token, start, end, line):
        return Token(
            INDENT,
            token[self.coloffset:],
            (self.lineno, start + self.coloffset),
            (self.lineno, end),
            line
        )

    def _dedenttoken(self, lineindent, line):
        return Token(
            DEDENT, '',
            (self.lineno, lineindent * self.indentsize + self.coloffset),
            (self.lineno, lineindent * self.indentsize + self.coloffset),
            line
        )

    def _newlinetoken(self, token, start, end, line):
        return Token(
            NEWLINE,
            token,
            (self.lineno, start),
            (self.lineno, end),
            line
        )

    def tokenizeline(self, line):
        self.lineno += 1

        if line == '':
            yield self._eoftoken(line)
            return

        for m in ALLTOKENS_RE.finditer(line):
            token = m.group()
            start, end = m.span()

            if token == '\\':  # Escape
                self.escape = True
                continue

            if self.escape:
                self.escape = False
                continue

            if self.newline and (start == 0):  # Beginning of line
                lineindent = 0
                if token.startswith(' '):  # Whitespace
                    # Indentation
                    if self.coloffset < 0:
                        self.coloffset = end

                    elif not self.indentsize:
                        self.indentsize = end - self.coloffset

                    if self.indentsize and (end > self.coloffset):
                        lineindent = (end - self.coloffset) // self.indentsize

                elif token not in ['\n'] and self.coloffset < 0:
                    self.coloffset = start

                if lineindent > self.indent:
                    self.indent = lineindent
                    yield self._indenttoken(token, start, end, line)

                elif lineindent < self.indent:
                    for i in range(self.indent - lineindent):
                        self.indent -= 1
                        yield self._dedenttoken(lineindent, line)

            if token.startswith(' '):  # Whitespace
                # Ignore for the now.
                continue

            self.newline = token == '\n'
            if self.newline:
                yield self._newlinetoken(token, start, end, line)
                continue

            yield Token(
                TOKENS_DICT.get(token, NAME),
                token,
                (self.lineno, start),
                (self.lineno, end),
                line
            )

    def tokenize(self, readline):
        eof = False

        while not eof:
            for token in self.tokenizeline(readline()):
                yield token
                eof = token.type == EOF

    def tokenizes(self, string):
        yield from self.tokenize(io.StringIO(string).readline)


def tokenizes(string):
    yield from Tokenizer().tokenizes(string)
