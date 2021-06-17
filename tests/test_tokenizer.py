from io import StringIO

import pytest

from dial.tokenizer import tokenize, EOF, AT, NAME, NL, COLON, DOT, LPAR, \
    RPAR, COMA, RARROW


def tokenizes(string):
    return tokenize(StringIO(string).readline)


def test_emptyinput():
    tokens = list(tokenizes(''))
    assert tokens[0] == (EOF, '', (1, 0), (1, 0), '')


def go(gen):
    t = next(gen)
    return t.type, t.string, t.start, t.end


def test_simple_call():
    gen = tokenizes(
        '@seq foo\n'
        'bar: baz\n'
        'bar: qux.quux(corge, fred) -> waldo'
    )
    assert go(gen) == (AT,     '@',     (1,  0), (1,  1))
    assert go(gen) == (NAME,   'seq',   (1,  1), (1,  4))
    assert go(gen) == (NAME,   'foo',   (1,  5), (1,  8))
    assert go(gen) == (NL,     '\n',    (1,  8), (1,  9))
    assert go(gen) == (NAME,   'bar',   (2,  0), (2,  3))
    assert go(gen) == (COLON,  ':',     (2,  3), (2,  4))
    assert go(gen) == (NAME,   'baz',   (2,  5), (2,  8))
    assert go(gen) == (NL,     '\n',    (2,  8), (2,  9))
    assert go(gen) == (NAME,   'bar',   (3,  0), (3,  3))
    assert go(gen) == (COLON,  ':',     (3,  3), (3,  4))
    assert go(gen) == (NAME,   'qux',   (3,  5), (3,  8))
    assert go(gen) == (DOT,    '.',     (3,  8), (3,  9))
    assert go(gen) == (NAME,   'quux',  (3,  9), (3, 13))
    assert go(gen) == (LPAR,   '(',     (3, 13), (3, 14))
    assert go(gen) == (NAME,   'corge', (3, 14), (3, 19))
    assert go(gen) == (COMA,   ',',     (3, 19), (3, 20))
    assert go(gen) == (NAME,   'fred',  (3, 21), (3, 25))
    assert go(gen) == (RPAR,   ')',     (3, 25), (3, 26))
    assert go(gen) == (RARROW, '->',    (3, 27), (3, 29))
    assert go(gen) == (NAME,   'waldo', (3, 30), (3, 35))
    assert go(gen) == (EOF,    '',      (4,  0), (4,  0))
    with pytest.raises(StopIteration):
        next(gen)
