from io import StringIO

from dial.tokenizer import tokenize, EOF, AT, NAME, NL, COLON


def tokenizes(string):
    return tokenize(StringIO(string).readline)


def test_emptyinput():
    tokens = list(tokenizes(''))
    assert tokens[0] == (EOF, '', (1, 0), (1, 0), '')


def test_simple_call():
    tokens = list(tokenizes(
        '@seq foo\n'
        'bar: baz'
    ))
    assert len(tokens) == 8
    assert tokens[0] == (AT,     '@',    (1, 0), (1, 1), '@seq foo\n')
    assert tokens[1] == (NAME,   'seq',  (1, 1), (1, 4), '@seq foo\n')
    assert tokens[2] == (NAME,   'foo',  (1, 5), (1, 8), '@seq foo\n')
    assert tokens[3] == (NL,     '\n',   (1, 8), (1, 9), '@seq foo\n')
    assert tokens[4] == (NAME,   'bar',  (2, 0), (2, 3), 'bar: baz')
    assert tokens[5] == (COLON,  ':',    (2, 3), (2, 4), 'bar: baz')
    assert tokens[6] == (NAME,   'baz',  (2, 5), (2, 8), 'bar: baz')
    assert tokens[7] == (EOF,    '',     (3, 0), (3, 0), '')
