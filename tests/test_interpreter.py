import pytest

from dial.tokenizer import Tokenizer
from dial.sequence import SequenceDiagram, Call, Module
from dial.interpreter import BadSyntax


def test_interpreter_sequencediagram_parse():
    d = SequenceDiagram(Tokenizer(), 'foo')

    d.parse('''
        foo: bar
        bar:
            baz
            qux
    ''')
    assert 'foo' in d.modules
    assert 'bar' in d.modules
    assert 'baz' in d.modules
    assert 'qux' in d.modules
    assert d[0] == Call('foo', 'bar')
    assert d[1] == Call('bar', 'baz')
    assert d[2] == Call('bar', 'qux')


def test_interpreter_sequencediagram_parseline():
    d = SequenceDiagram(Tokenizer(), 'foo')

    d.parseline('foo: bar')
    assert isinstance(d.modules['foo'], Module)
    assert isinstance(d.modules['bar'], Module)
    assert d.modules['foo'].name == 'foo'
    assert d.modules['bar'].name == 'bar'
    assert isinstance(d[0], Call)
    assert d[0].caller == 'foo'
    assert d[0].callee == 'bar'

    d.parseline('\n')
    assert d.state == d.states['root']


def test_interpreter_badsyntax():
    d = SequenceDiagram(Tokenizer(), 'foo')
    with pytest.raises(BadSyntax) as e:
        d.parseline('foo')
    assert str(e.value) == '''\
File "String", line 1, col 3
Expected: COLON, got: NEWLINE.'''

    d = SequenceDiagram(Tokenizer(), 'foo')
    with pytest.raises(BadSyntax) as e:
        d.parseline('foo: @')
    assert str(e.value) == '''\
File "String", line 1, col 5
Expected one of: (NAME|NEWLINE), got: AT "@".'''

    d = SequenceDiagram(Tokenizer(), 'foo')
    d.parseline('foo: ')
    with pytest.raises(BadSyntax) as e:
        d.parseline('')
    assert str(e.value) == '''\
File "String", line 2, col 0
Expected: INDENT, got: EOF.'''
