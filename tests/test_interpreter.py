import pytest

from dial.tokenizer import Tokenizer
from dial.sequence import SequenceDiagram
from dial.interpreter import BadSyntax


def test_sequence_calltext():
    d = SequenceDiagram(Tokenizer(), 'foo')
    s = '''# Sequence
foo -> bar: baz
foo -> bar: int baz.qux(quux):int
  bar -> baz: thud
    foo -> bar
      foo -> bar: 123 !@#$%^&*() {}[];',./?><"\\|
foo -> bar
'''
    d.parse(s)
    assert repr(d) == s[:-1]


def test_sequence_hierarchy():
    d = SequenceDiagram(Tokenizer(), 'foo')
    s = '''# Sequence
foo -> bar
foo -> baz
  baz -> qux
    qux -> bar
      qux -> bar
    qux -> bar
  baz -> qux
foo -> bar
'''
    d.parse(s)
    assert repr(d) == s[:-1]


def test_interpreter_badsyntax():
    d = SequenceDiagram(Tokenizer(), 'foo')
    with pytest.raises(BadSyntax) as e:
        d.parse('foo')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 0
Expected `->`, got: EOF.\
'''

    d = SequenceDiagram(Tokenizer(), 'foo')
    with pytest.raises(BadSyntax) as e:
        d.parse('foo::')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 1, col 3
Expected `->`, got: COLON ":".\
'''

    d = SequenceDiagram(Tokenizer(), 'foo')
    with pytest.raises(BadSyntax) as e:
        d.parse('''
            foo:
            bar
        ''')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 15
Expected `->`, got: COLON ":".\
'''
    d = SequenceDiagram(Tokenizer(), 'foo')
    with pytest.raises(BadSyntax) as e:
        d.parse('foo: bar: baz')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 1, col 3
Expected `->`, got: COLON ":".\
'''
