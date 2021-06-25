import pytest

from dial.tokenizer import Tokenizer
from dial.sequence import SequenceDiagram
from dial.interpreter import BadSyntax, BadAttribute


def test_sequence_note():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
title: note

@over: |
  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
  tempor incididunt ut labore et dolore.

@over ~: Foo Bar baz
@over foo ~ bar: Foo Bar baz
@over ~ foo: Foo Bar baz
@over foo ~: Foo Bar baz
@over: Foo Bar baz
@over foo: Foo Bar baz
@right of qux: note
@left of bar: note
'''
    d.parse(s)
    assert repr(d) == s[:-1]


def test_sequence_condition():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
title: condition

if: foo > 1
  foo -> bar: baz(*)
elif: foo < 0
else
  alt: j > 9
    foo -> bar: baz(*)
  else
    foo -> bar: baz(*)
'''
    d.parse(s)
    assert repr(d) == s[:-1]


def test_sequence_loop():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
title: loop

foo -> bar
  loop: over list
    bar -> baz
for
  foo -> bar: baz(*)
for: i in range(10)
  foo -> bar: baz(i)
while: j > 0
  foo -> bar: baz(j)
loop: over [1, 2, 3]
  for: i in list(7...99)
    while: bool
      foo -> thud: wow
'''
    d.parse(s)
    assert repr(d) == s[:-1]


def test_sequence_comment():
    d = SequenceDiagram(Tokenizer())
    s = '''# Sequence
title: Comment

# This is comment
foo -> bar:
  # This is comment too
'''
    d.parse(s)
    assert repr(d) == '''# Sequence
title: Comment

foo -> bar'''


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
