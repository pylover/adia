# flake8: noqa: E241
import io

from adia.token import *
from adia.tokenizer import Tokenizer

from .helpers import raises


def tokenize(string):
    tokenizer = Tokenizer()

    with io.StringIO(string) as f:
        while True:
            line = f.readline()
            for t in tokenizer.feedline(line):
                yield t.type, t.string, t.start, t.end

            if not line:
                break


def test_tokenizer_hash():
    exp = 'foo bar.baz(a, b): as return'
    gen = tokenize(f'#{exp}\n  foo')
    assert next(gen) == (HASH,       '#',   (1,  0), (1,  1))
    assert next(gen) == (EVERYTHING, exp,   (1,  1), (1, 29))
    assert next(gen) == (NEWLINE,    '\n',  (1, 29), (1, 30))
    assert next(gen) == (INDENT,     '  ',  (2,  0), (2,  2))
    assert next(gen) == (NAME,      'foo',  (2,  2), (2,  5))
    assert next(gen) == (EOF,        '',    (3,  0), (3,  0))
    with raises(StopIteration):
        next(gen)


def test_tokenizer_colon():
    exp = 'foo bar.baz(a, b): as return'
    gen = tokenize(f':{exp}\n  foo')
    assert next(gen) == (COLON,      ':',   (1,  0), (1,  1))
    assert next(gen) == (EVERYTHING, exp,   (1,  1), (1, 29))
    assert next(gen) == (NEWLINE,    '\n',  (1, 29), (1, 30))
    assert next(gen) == (INDENT,     '  ',  (2,  0), (2,  2))
    assert next(gen) == (NAME,      'foo',  (2,  2), (2,  5))
    assert next(gen) == (EOF,        '',    (3,  0), (3,  0))
    with raises(StopIteration):
        next(gen)


def test_tokenizer_multiline():
    gen = tokenize('''
    |
        foo
        bar.
    foo bar
    ''')
    exp = 'foo\nbar.'
    assert next(gen) == (NEWLINE,   '\n',  (1,  0), (1,  1))
    assert next(gen) == (MULTILINE, exp,   (3,  8), (4, 12))
    assert next(gen) == (NAME,      'foo', (5,  4), (5,  7))
    assert next(gen) == (NAME,      'bar', (5,  8), (5, 11))
    assert next(gen) == (NEWLINE,   '\n',  (5, 11), (5, 12))
    assert next(gen) == (EOF,       '',    (7,  0), (7,  0))
    with raises(StopIteration):
        next(gen)

    gen = tokenize('''
    | foo
    ''')
    assert next(gen) == (NEWLINE,   '\n',  (1,  0), (1,  1))
    assert next(gen) == (PIPE,      '|',   (2,  4), (2,  5))
    assert next(gen) == (NAME,      'foo', (2,  6), (2,  9))
    assert next(gen) == (NEWLINE,   '\n',  (2,  9), (2, 10))
    assert next(gen) == (EOF,       '',    (4,  0), (4,  0))
    with raises(StopIteration):
        next(gen)


def test_tokenizer_emptyinput():
    gen = tokenize('')
    assert next(gen) == (EOF,     '',   (1, 0), (1, 0))
    with raises(StopIteration):
        next(gen)


def test_tokenizer_indentation():
    gen = tokenize(
        'foo\n'
        '  bar\n'
        '    thud\n'
        '  baz\n'
        '    fred\n'
        '      corge\n'
        'qux quux'
    )
    assert next(gen) == (NAME,    'foo',  (1,  0), (1,  3))
    assert next(gen) == (NEWLINE, '\n',   (1,  3), (1,  4))
    assert next(gen) == (INDENT,  '  ',   (2,  0), (2,  2))
    assert next(gen) == (NAME,    'bar',  (2,  2), (2,  5))
    assert next(gen) == (NEWLINE, '\n',   (2,  5), (2,  6))
    assert next(gen) == (INDENT,  '  ',   (3,  2), (3,  4))
    assert next(gen) == (NAME,    'thud', (3,  4), (3,  8))
    assert next(gen) == (NEWLINE, '\n',   (3,  8), (3,  9))
    assert next(gen) == (DEDENT,  '',     (4,  2), (4,  2))
    assert next(gen) == (NAME,    'baz',  (4,  2), (4,  5))
    assert next(gen) == (NEWLINE, '\n',   (4,  5), (4,  6))
    assert next(gen) == (INDENT,  '  ',   (5,  2), (5,  4))
    assert next(gen) == (NAME,    'fred', (5,  4), (5,  8))
    assert next(gen) == (NEWLINE, '\n',   (5,  8), (5,  9))
    assert next(gen) == (INDENT,  '  ',   (6,  4), (6,  6))
    assert next(gen) == (NAME,    'corge',(6,  6), (6, 11))
    assert next(gen) == (NEWLINE, '\n',   (6, 11), (6, 12))
    assert next(gen) == (DEDENT,  '',     (7,  0), (7,  0))
    assert next(gen) == (DEDENT,  '',     (7,  0), (7,  0))
    assert next(gen) == (DEDENT,  '',     (7,  0), (7,  0))
    assert next(gen) == (NAME,    'qux',  (7,  0), (7,  3))
    assert next(gen) == (NAME,    'quux', (7,  4), (7,  8))
    assert next(gen) == (EOF,     '',     (8,  0), (8,  0))
    with raises(StopIteration):
        next(gen)


def test_tokenizer_indentation_autocoloffset():
    gen = tokenize('''
        foo bar
        bar
            baz
            qux

                quux
    ''')
    assert next(gen) == (NEWLINE, '\n',   (1,  0), (1,  1))
    assert next(gen) == (NAME,    'foo',  (2,  8), (2, 11))
    assert next(gen) == (NAME,    'bar',  (2, 12), (2, 15))
    assert next(gen) == (NEWLINE, '\n',   (2, 15), (2, 16))
    assert next(gen) == (NAME,    'bar',  (3,  8), (3, 11))
    assert next(gen) == (NEWLINE, '\n',   (3, 11), (3, 12))
    assert next(gen) == (INDENT,  '    ', (4,  8), (4, 12))
    assert next(gen) == (NAME,    'baz',  (4, 12), (4, 15))
    assert next(gen) == (NEWLINE, '\n',   (4, 15), (4, 16))
    assert next(gen) == (NAME,    'qux',  (5, 12), (5, 15))
    assert next(gen) == (NEWLINE, '\n',   (5, 15), (5, 16))
    assert next(gen) == (DEDENT,  '',     (6,  8), (6,  8))
    assert next(gen) == (NEWLINE, '\n',   (6,  0), (6,  1))
    assert next(gen) == (INDENT,  '    ', (7,  8), (7, 12))
    assert next(gen) == (INDENT,  '    ', (7, 12), (7, 16))
    assert next(gen) == (NAME,    'quux', (7, 16), (7, 20))
    assert next(gen) == (NEWLINE, '\n',   (7, 20), (7, 21))
    assert next(gen) == (DEDENT,  '',     (8,  8), (8,  8))
    assert next(gen) == (DEDENT,  '',     (8,  8), (8,  8))
    assert next(gen) == (EOF,     '',     (9,  0), (9,  0))
    with raises(StopIteration):
        next(gen)

    gen = tokenize('''
        foo bar
    ''')
    assert next(gen) == (NEWLINE, '\n',   (1,  0), (1,  1))
    assert next(gen) == (NAME,    'foo',  (2,  8), (2, 11))
    assert next(gen) == (NAME,    'bar',  (2, 12), (2, 15))
    assert next(gen) == (NEWLINE, '\n',   (2, 15), (2, 16))
    assert next(gen) == (EOF,     '',     (4,  0), (4,  0))
    with raises(StopIteration):
        next(gen)

    # Automatic column offset detection
    gen = tokenize('''
        foo
          bar
        qux quux''')
    assert next(gen) == (NEWLINE, '\n',   (1,  0), (1,  1))
    assert next(gen) == (NAME,    'foo',  (2,  8), (2, 11))
    assert next(gen) == (NEWLINE, '\n',   (2, 11), (2, 12))
    assert next(gen) == (INDENT,  '  ',   (3,  8), (3, 10))
    assert next(gen) == (NAME,    'bar',  (3, 10), (3, 13))
    assert next(gen) == (NEWLINE, '\n',   (3, 13), (3, 14))
    assert next(gen) == (DEDENT,  '',     (4,  8), (4,  8))
    assert next(gen) == (NAME,    'qux',  (4,  8), (4, 11))
    assert next(gen) == (NAME,    'quux', (4, 12), (4, 16))
    assert next(gen) == (EOF,     '',     (5,  0), (5,  0))
    with raises(StopIteration):
        next(gen)

    gen = tokenize('''
      foo
        bar
      qux quux''')
    assert next(gen) == (NEWLINE, '\n',   (1,  0), (1,  1))
    assert next(gen) == (NAME,    'foo',  (2,  6), (2,  9))
    assert next(gen) == (NEWLINE, '\n',   (2,  9), (2, 10))
    assert next(gen) == (INDENT,  '  ',   (3,  6), (3,  8))
    assert next(gen) == (NAME,    'bar',  (3,  8), (3, 11))
    assert next(gen) == (NEWLINE, '\n',   (3, 11), (3, 12))
    assert next(gen) == (DEDENT,  '',     (4,  6), (4,  6))
    assert next(gen) == (NAME,    'qux',  (4,  6), (4,  9))
    assert next(gen) == (NAME,    'quux', (4, 10), (4, 14))
    assert next(gen) == (EOF,     '',     (5,  0), (5,  0))
    with raises(StopIteration):
        next(gen)


def test_tokenizer_escapechar():
    gen = tokenize('\\@ \\: \\|')
    assert next(gen) == (NAME,      '@',     (1,  1), (1,  2))
    assert next(gen) == (NAME,      ':',     (1,  4), (1,  5))
    assert next(gen) == (NAME,      '|',     (1,  7), (1,  8))
    assert next(gen) == (EOF,       '',      (2,  0), (2,  0))
    with raises(StopIteration):
        next(gen)

    gen = tokenize('\\\n \n')
    assert next(gen) == (NEWLINE,   '\n',    (2,  0), (2,  1))
    assert next(gen) == (EOF,       '',      (3,  0), (3,  0))
    with raises(StopIteration):
        next(gen)

    gen = tokenize('\\\\')
    assert next(gen) == (BACKSLASH, '\\',    (1,  1), (1,  2))
    assert next(gen) == (EOF,       '',      (2,  0), (2,  0))
    with raises(StopIteration):
        next(gen)

    gen = tokenize(
        'foo\\\n'
        '  bar\\\n.baz'
    )
    assert next(gen) == (NAME,    'foo',   (1,  0), (1,  3))
    assert next(gen) == (NAME,    'bar',   (2,  2), (2,  5))
    assert next(gen) == (DOT,     '.',     (3,  0), (3,  1))
    assert next(gen) == (NAME,    'baz',   (3,  1), (3,  4))
    assert next(gen) == (EOF,     '',      (4,  0), (4,  0))
    with raises(StopIteration):
        next(gen)


def test_space_at_emptyline_issue46():
    gen = tokenize('foo\n  \nbar')
    assert next(gen) == (NAME,    'foo', (1,  0), (1,  3))
    assert next(gen) == (NEWLINE, '\n',  (1,  3), (1,  4))
    assert next(gen) == (NEWLINE, '\n',  (2,  0), (2,  1))
    assert next(gen) == (NAME,    'bar', (3,  0), (3,  3))
    assert next(gen) == (EOF,     '',    (4,  0), (4,  0))
    with raises(StopIteration):
        next(gen)


def test_class_diagram():
    gen = tokenize('''
        Foo(Bar, Baz)
          int bar
          + qux -> Qux
          ---
    ''')
    assert next(gen) == (NEWLINE, '\n',    (1,  0), (1,  1))
    assert next(gen) == (NAME,    'Foo',   (2,  8), (2, 11))
    assert next(gen) == (LPAR,    '(',     (2, 11), (2, 12))
    assert next(gen) == (NAME,    'Bar',   (2, 12), (2, 15))
    assert next(gen) == (COMMA,   ',',     (2, 15), (2, 16))
    assert next(gen) == (NAME,    'Baz',   (2, 17), (2, 20))
    assert next(gen) == (RPAR,    ')',     (2, 20), (2, 21))
    assert next(gen) == (NEWLINE, '\n',    (2, 21), (2, 22))
    assert next(gen) == (INDENT,  '  ',    (3,  8), (3, 10))
    assert next(gen) == (NAME,    'int',   (3, 10), (3, 13))
    assert next(gen) == (NAME,    'bar',   (3, 14), (3, 17))
    assert next(gen) == (NEWLINE, '\n',    (3, 17), (3, 18))
    assert next(gen) == (PLUS,    '+',     (4, 10), (4, 11))
    assert next(gen) == (NAME,    'qux',   (4, 12), (4, 15))
    assert next(gen) == (RARROW,  '->',    (4, 16), (4, 18))
    assert next(gen) == (NAME,    'Qux',   (4, 19), (4, 22))
    assert next(gen) == (NEWLINE, '\n',    (4, 22), (4, 23))
    assert next(gen) == (HSEP,    '---',   (5, 10), (5, 13))
    assert next(gen) == (NEWLINE, '\n',    (5, 13), (5, 14))
    assert next(gen) == (DEDENT,  '',      (6,  8), (6,  8))
    assert next(gen) == (EOF,     '',      (7,  0), (7,  0))
    with raises(StopIteration):
        next(gen)


