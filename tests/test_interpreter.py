import pytest

from dial.tokenizer import Tokenizer
from dial.sequence import SequenceDiagram, Call, Module
from dial.interpreter import BadSyntax


def test_interpreter_sequencediagram_indent():
    d = SequenceDiagram(Tokenizer(), 'foo')
    d.parse('''
        foo()
        foo:
            baz()
            bar:
                baz
                qux
            baz:
                qux:
                    phoenix.fly(sky, space)
                thud
            giga.mega(alef)
        foo: bar
''')
    assert 'foo' in d.modules
    assert 'bar' in d.modules
    assert 'baz' in d.modules
    assert 'qux' in d.modules
    assert 'giga' in d.modules
    assert 'thud' in d.modules
    assert 'phoenix' in d.modules
    assert repr(d[0]) == 'foo -> foo'
    assert repr(d[1]) == 'foo -> foo.baz()'
    assert repr(d[2]) == \
        'foo -> bar:\n' \
        '  bar -> baz\n' \
        '  bar -> qux'
    assert repr(d[3]) ==  \
        'foo -> baz:\n' \
        '  baz -> qux:\n' \
        '    qux -> phoenix.fly(sky, space)\n' \
        '  baz -> thud'
    assert repr(d[4]) == 'foo -> giga.mega(alef)'
    assert repr(d[5]) == 'foo -> bar'
    assert len(d) == 6


def test_interpreter_sequencediagram_callargs():
    d = SequenceDiagram(Tokenizer(), 'foo')
    d.parse('''
        foo: bar
        foo: bar.baz()
        foo.baz(): bar
        foo.baz(): bar.baz()
        foo.baz(a, b): bar.baz(c)
        foo:
            bar
            baz.thud(a, b, c)
        foo: bar
''')
    assert 'foo' in d.modules
    assert 'bar' in d.modules
    assert 'baz' in d.modules
    assert repr(d[0]) == 'foo -> bar'
    assert repr(d[1]) == 'foo -> bar.baz()'
    assert repr(d[2]) == 'foo.baz() -> bar'
    assert repr(d[3]) == 'foo.baz() -> bar.baz()'
    assert repr(d[4]) == 'foo.baz(a, b) -> bar.baz(c)'
    assert repr(d[5]) == 'foo -> bar'
    assert repr(d[6]) == 'foo -> baz.thud(a, b, c)'
    assert repr(d[7]) == 'foo -> bar'
    assert len(d) == 8


def test_interpreter_sequencediagram_parseline():
    d = SequenceDiagram(Tokenizer(), 'foo')

    d.parseline('foo: bar')
    assert isinstance(d.modules['foo'], Module)
    assert isinstance(d.modules['bar'], Module)
    assert d.modules['foo'].name == 'foo'
    assert d.modules['bar'].name == 'bar'
    assert isinstance(d[0], Call)
    assert repr(d[0]) == 'foo -> bar'

    d.parseline('\n')
    assert d.state == d.states['start']


def test_interpreter_badsyntax():
    d = SequenceDiagram(Tokenizer(), 'foo')
    with pytest.raises(BadSyntax) as e:
        d.parse('foo')
    assert str(e.value) == '''\
File "String", line 2, col 0
Expected one of `:|.|NEWLINE|(`, got: EOF.'''

    d = SequenceDiagram(Tokenizer(), 'foo')
    with pytest.raises(BadSyntax) as e:
        d.parse('foo::')
    assert str(e.value) == '''\
File "String", line 1, col 4
Expected one of `NAME|NEWLINE`, got: COLON ":".'''

    d = SequenceDiagram(Tokenizer(), 'foo')
    with pytest.raises(BadSyntax) as e:
        d.parse('''
            foo:
            bar
        ''')
    assert str(e.value) == '''\
File "String", line 3, col 12
Expected `INDENT`, got: NAME "bar".'''
