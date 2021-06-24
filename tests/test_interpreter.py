import pytest

from dial.tokenizer import Tokenizer
from dial.sequence import SequenceDiagram, Call, Module
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


# def test_interpreter_badsyntax():
#     d = SequenceDiagram(Tokenizer(), 'foo')
#     with pytest.raises(BadSyntax) as e:
#         d.parse('foo')
#     assert str(e.value) == '''\
# File "String", line 2, col 0
# Expected one of `NAME|:|.|NEWLINE|(`, got: EOF.'''
# 
#     d = SequenceDiagram(Tokenizer(), 'foo')
#     with pytest.raises(BadSyntax) as e:
#         d.parse('foo::')
#     assert str(e.value) == '''\
# File "String", line 1, col 4
# Expected one of `NAME|NEWLINE|MULTILINE`, got: COLON ":".'''
# 
#     d = SequenceDiagram(Tokenizer(), 'foo')
#     with pytest.raises(BadSyntax) as e:
#         d.parse('''
#             foo:
#             bar
#         ''')
#     assert str(e.value) == '''\
# File "String", line 3, col 12
# Expected `INDENT`, got: NAME "bar".'''
# 
#     d = SequenceDiagram(Tokenizer(), 'foo')
#     with pytest.raises(BadSyntax) as e:
#         d.parse('foo: bar: baz')
#     assert str(e.value) == '''\
# File "String", line 2, col 0
# Expected one of `NAME|:|.|NEWLINE|(`, got: EOF.'''
