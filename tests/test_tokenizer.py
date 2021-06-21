import pytest

from dial.token import *
from dial.tokenizer import tokenizes as tokenizes_


def tokenizes(string):
    for t in tokenizes_(string):
        yield t.type, t.string, t.start, t.end


def test_tokenizer_emptyinput():
    gen = tokenizes('')
    assert next(gen) == (EOF, '', (1, 0), (1, 0))
    with pytest.raises(StopIteration):
        next(gen)


def test_tokenizer_sequencediagram_flat():
    gen = tokenizes(
        '@seq foo\n'
        'bar: baz\n'
        'bar: qux.quux(corge, fred) -> waldo'
    )
    assert next(gen) == (AT,      '@',     (1,  0), (1,  1))
    assert next(gen) == (NAME,    'seq',   (1,  1), (1,  4))
    assert next(gen) == (NAME,    'foo',   (1,  5), (1,  8))
    assert next(gen) == (NEWLINE, '\n',    (1,  8), (1,  9))
    assert next(gen) == (NAME,    'bar',   (2,  0), (2,  3))
    assert next(gen) == (COLON,   ':',     (2,  3), (2,  4))
    assert next(gen) == (NAME,    'baz',   (2,  5), (2,  8))
    assert next(gen) == (NEWLINE, '\n',    (2,  8), (2,  9))
    assert next(gen) == (NAME,    'bar',   (3,  0), (3,  3))
    assert next(gen) == (COLON,   ':',     (3,  3), (3,  4))
    assert next(gen) == (NAME,    'qux',   (3,  5), (3,  8))
    assert next(gen) == (DOT,     '.',     (3,  8), (3,  9))
    assert next(gen) == (NAME,    'quux',  (3,  9), (3, 13))
    assert next(gen) == (LPAR,    '(',     (3, 13), (3, 14))
    assert next(gen) == (NAME,    'corge', (3, 14), (3, 19))
    assert next(gen) == (COMMA,   ',',     (3, 19), (3, 20))
    assert next(gen) == (NAME,    'fred',  (3, 21), (3, 25))
    assert next(gen) == (RPAR,    ')',     (3, 25), (3, 26))
    assert next(gen) == (RARROW,  '->',    (3, 27), (3, 29))
    assert next(gen) == (NAME,    'waldo', (3, 30), (3, 35))
    assert next(gen) == (EOF,     '',      (4,  0), (4,  0))
    with pytest.raises(StopIteration):
        next(gen)


def test_tokenizer_sequencediagram_indented():
    gen = tokenizes(
        'foo:\n'
        '  bar:\n'
        '    thud\n'
        '  baz:\n'
        '    fred:\n'
        '      corge\n'
        'qux: quux'
    )
    assert next(gen) == (NAME,    'foo',    (1,  0), (1,  3))
    assert next(gen) == (COLON,   ':',      (1,  3), (1,  4))
    assert next(gen) == (NEWLINE, '\n',     (1,  4), (1,  5))
    assert next(gen) == (INDENT,  '  ',     (2,  0), (2,  2))
    assert next(gen) == (NAME,    'bar',    (2,  2), (2,  5))
    assert next(gen) == (COLON,   ':',      (2,  5), (2,  6))
    assert next(gen) == (NEWLINE, '\n',     (2,  6), (2,  7))
    assert next(gen) == (INDENT,  '    ',   (3,  0), (3,  4))
    assert next(gen) == (NAME,    'thud',   (3,  4), (3,  8))
    assert next(gen) == (NEWLINE, '\n',     (3,  8), (3,  9))
    assert next(gen) == (DEDENT,  '',       (4,  2), (4,  2))
    assert next(gen) == (NAME,    'baz',    (4,  2), (4,  5))
    assert next(gen) == (COLON,   ':',      (4,  5), (4,  6))
    assert next(gen) == (NEWLINE, '\n',     (4,  6), (4,  7))
    assert next(gen) == (INDENT,  '    ',   (5,  0), (5,  4))
    assert next(gen) == (NAME,    'fred',   (5,  4), (5,  8))
    assert next(gen) == (COLON,   ':',      (5,  8), (5,  9))
    assert next(gen) == (NEWLINE, '\n',     (5,  9), (5, 10))
    assert next(gen) == (INDENT,  '      ', (6,  0), (6,  6))
    assert next(gen) == (NAME,    'corge',  (6,  6), (6, 11))
    assert next(gen) == (NEWLINE, '\n',     (6, 11), (6, 12))
    assert next(gen) == (DEDENT,  '',       (7,  0), (7,  0))
    assert next(gen) == (DEDENT,  '',       (7,  0), (7,  0))
    assert next(gen) == (DEDENT,  '',       (7,  0), (7,  0))
    assert next(gen) == (NAME,    'qux',    (7,  0), (7,  3))
    assert next(gen) == (COLON,   ':',      (7,  3), (7,  4))
    assert next(gen) == (NAME,    'quux',   (7,  5), (7,  9))
    assert next(gen) == (EOF,     '',       (8,  0), (8,  0))
    with pytest.raises(StopIteration):
        next(gen)


def test_tokenizer_sequencediagram_indented_autocoloffset():
    gen = tokenizes('''
        foo: bar
        bar:
            baz
            qux
    ''')
    assert next(gen) == (NEWLINE, '\n',   (1,  0), (1,  1))
    assert next(gen) == (NAME,    'foo',  (2,  8), (2, 11))
    assert next(gen) == (COLON,   ':',    (2, 11), (2, 12))
    assert next(gen) == (NAME,    'bar',  (2, 13), (2, 16))
    assert next(gen) == (NEWLINE, '\n',   (2, 16), (2, 17))
    assert next(gen) == (NAME,    'bar',  (3,  8), (3, 11))
    assert next(gen) == (COLON,   ':',    (3, 11), (3, 12))
    assert next(gen) == (NEWLINE, '\n',   (3, 12), (3, 13))
    assert next(gen) == (INDENT,  '    ', (4,  8), (4, 12))
    assert next(gen) == (NAME,    'baz',  (4, 12), (4, 15))
    assert next(gen) == (NEWLINE, '\n',   (4, 15), (4, 16))
    assert next(gen) == (NAME,    'qux',  (5, 12), (5, 15))
    assert next(gen) == (NEWLINE, '\n',   (5, 15), (5, 16))
    assert next(gen) == (DEDENT,  '',     (6,  8), (6,  8))
    assert next(gen) == (EOF,     '',     (7,  0), (7,  0))
    with pytest.raises(StopIteration):
        next(gen)

    gen = tokenizes('''
        foo: bar
    ''')
    assert next(gen) == (NEWLINE, '\n',   (1,  0), (1,  1))
    assert next(gen) == (NAME,    'foo',  (2,  8), (2, 11))
    assert next(gen) == (COLON,   ':',    (2, 11), (2, 12))
    assert next(gen) == (NAME,    'bar',  (2, 13), (2, 16))
    assert next(gen) == (NEWLINE, '\n',   (2, 16), (2, 17))
    assert next(gen) == (EOF,     '',     (4,  0), (4,  0))
    with pytest.raises(StopIteration):
        next(gen)

    # Automatic column offset detection
    gen = tokenizes('''
        foo:
          bar
        qux: quux''')
    assert next(gen) == (NEWLINE, '\n',   (1,  0), (1,  1))
    assert next(gen) == (NAME,    'foo',  (2,  8), (2, 11))
    assert next(gen) == (COLON,   ':',    (2, 11), (2, 12))
    assert next(gen) == (NEWLINE, '\n',   (2, 12), (2, 13))
    assert next(gen) == (INDENT,  '  ',   (3,  8), (3, 10))
    assert next(gen) == (NAME,    'bar',  (3, 10), (3, 13))
    assert next(gen) == (NEWLINE, '\n',   (3, 13), (3, 14))
    assert next(gen) == (DEDENT,  '',     (4,  8), (4,  8))
    assert next(gen) == (NAME,    'qux',  (4,  8), (4, 11))
    assert next(gen) == (COLON,   ':',    (4, 11), (4, 12))
    assert next(gen) == (NAME,    'quux', (4, 13), (4, 17))
    assert next(gen) == (EOF,     '',     (5,  0), (5,  0))
    with pytest.raises(StopIteration):
        next(gen)

    gen = tokenizes('''
      foo:
        bar
      qux: quux''')
    assert next(gen) == (NEWLINE, '\n',   (1,  0), (1,  1))
    assert next(gen) == (NAME,    'foo',  (2,  6), (2,  9))
    assert next(gen) == (COLON,   ':',    (2,  9), (2, 10))
    assert next(gen) == (NEWLINE, '\n',   (2, 10), (2, 11))
    assert next(gen) == (INDENT,  '  ',   (3,  6), (3,  8))
    assert next(gen) == (NAME,    'bar',  (3,  8), (3, 11))
    assert next(gen) == (NEWLINE, '\n',   (3, 11), (3, 12))
    assert next(gen) == (DEDENT,  '',     (4,  6), (4,  6))
    assert next(gen) == (NAME,    'qux',  (4,  6), (4,  9))
    assert next(gen) == (COLON,   ':',    (4,  9), (4, 10))
    assert next(gen) == (NAME,    'quux', (4, 11), (4, 15))
    assert next(gen) == (EOF,     '',     (5,  0), (5,  0))
    with pytest.raises(StopIteration):
        next(gen)


def test_tokenizer_escapechar():
    gen = tokenizes(
        'foo:\\\n'
        '  bar\\\n.baz'
    )
    assert next(gen) == (NAME,   'foo',   (1, 0), (1, 3))
    assert next(gen) == (COLON,  ':',     (1, 3), (1, 4))
    assert next(gen) == (NAME,   'bar',   (2, 2), (2, 5))
    assert next(gen) == (DOT,    '.',     (3, 0), (3, 1))
    assert next(gen) == (NAME,   'baz',   (3, 1), (3, 4))
    assert next(gen) == (EOF,    '',      (4, 0), (4, 0))
    with pytest.raises(StopIteration):
        next(gen)
