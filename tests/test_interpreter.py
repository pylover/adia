import pytest

from dial.tokenizer import Tokenizer
from dial.sequence import SequenceDiagram
from dial.interpreter import BadSyntax, BadAttribute


def test_sequence_comment():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
# This is comment
'''
    d.parse(s)
    assert repr(d) == '''# Sequence
title: Untitled'''


def test_sequence_moduleattr_error():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
foo.invalid: Foo
'''
    with pytest.raises(BadAttribute) as e:
        d.parse(s)
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 16
Invalid attribute: foo.invalid.\
'''


def test_sequence_moduleattr():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
title: Foo Bar

foo.title: Foo
foo.type: Actor
bar.title: Bar

foo -> bar: baz
'''
    d.parse(s)
    assert repr(d) == s[:-1]


def test_sequence_title_error():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
invalid: Foo Bar

foo -> bar: baz
'''
    with pytest.raises(BadAttribute) as e:
        d.parse(s)
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 16
Invalid attribute: invalid.\
'''


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
        d.parseline('foo')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 1, col 3
Expected one of `->|:|.`, got: NEWLINE.\
'''

    d = SequenceDiagram(Tokenizer())
    with pytest.raises(BadSyntax) as e:
        d.parse('''
            foo
            bar
        ''')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 15
Expected one of `->|:|.`, got: NEWLINE.\
'''

    d = SequenceDiagram(Tokenizer())
    with pytest.raises(BadSyntax) as e:
        d.parse('''
            title: Foo
              foo: bar
        ''')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 3, col 17
Expected `->`, got: COLON ":".\
'''
