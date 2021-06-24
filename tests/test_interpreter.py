import pytest

from dial.tokenizer import Tokenizer
from dial.sequence import SequenceDiagram
from dial.interpreter import BadSyntax


def test_sequence_title():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
title: Foo Bar

foo -> bar: baz
'''
    d.parse(s)
    assert repr(d) == s[:-1]


def test_sequence_calltext():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
title: Foo Bar

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
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
title: Foo Bar

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
    d = SequenceDiagram(Tokenizer())
    with pytest.raises(BadSyntax) as e:
        d.parse('foo')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 0
Expected one of `->|:`, got: EOF.\
'''

    d = SequenceDiagram(Tokenizer())
    with pytest.raises(BadSyntax) as e:
        d.parse('''
            foo
            bar
        ''')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 15
Expected one of `->|:`, got: NEWLINE.\
'''
