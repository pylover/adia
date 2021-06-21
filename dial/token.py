from collections import namedtuple


__all__ = ['Token', 'EXACT_TOKENS', 'TOKEN_NAMES']


EOF = 0
NAME = 1
NEWLINE = 2
AT = 3
DOT = 4
COLON = 5
LPAR = 6
RPAR = 7
COMMA = 8
RARROW = 9
INDENT = 10
DEDENT = 11
BACKSLASH = 12


TOKEN_NAMES = {
    value: name for name, value in globals().items()
    if isinstance(value, int) and not name.startswith('_')
}


__all__.extend(TOKEN_NAMES.values())


EXACT_TOKENS = [
    ('->', RARROW),
    ('@',  AT),
    ('.',  DOT),
    (':',  COLON),
    ('(',  LPAR),
    (')',  RPAR),
    (',',  COMMA),
    ('\\', BACKSLASH),
]
EXACT_TOKENS_DICT = {value: string for string, value in EXACT_TOKENS}


# Token namedtuple
class Token(namedtuple('Token', 'type string start end line')):
    def __repr__(self):
        return f'Token({TOKEN_NAMES[self.type]}, {self.string}, ' \
            f'{self.start}, {self.end}, {self.line})'
