import pytest

from dial.exceptions import BadSyntax, BadAttribute
from dial.sequence import SequenceDiagram


def test_sequenceitem_repr():
    s = '''# Sequence
title: foo

foo -> bar
foo -> bar:
foo -> bar: baz
for: i in range(10)
  foo -> baz
'''
    d = SequenceDiagram.loads(s)
    assert repr(d[0]) == 'foo -> bar'
    assert repr(d[1]) == 'foo -> bar'
    assert repr(d[2]) == 'foo -> bar: baz'
    assert repr(d[3]) == 'for: i in range(10)'


def test_sequence_repr():
    s = '''# Sequence
title: foo
'''
    d = SequenceDiagram.loads(s)
    assert repr(d) == 'SequenceDiagram: foo'


def test_sequence_note():
    s = '''# Sequence
title: note

@over: |
  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
  tempor incididunt ut labore et dolore.

@over ~: Foo Bar baz
@over ~ foo: Foo Bar baz
@over thud ~ bar: Foo Bar baz
@over foo ~: Foo Bar baz
@over: Foo Bar baz
@over foo: Foo Bar baz
@right of qux: note
foo -> bar
  @left of bar: note
  baz -> quux: f()
'''
    d = SequenceDiagram.loads(s)
    assert d.dumps() == s[:-1]
    assert 'thud' in d.modules
    assert 'bar' in d.modules
    assert 'baz' in d.modules
    assert 'foo' in d.modules
    assert 'qux' in d.modules
    assert 'quux' in d.modules


def test_sequence_condition():
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
      if: fred
        fred -> quux
'''
    d = SequenceDiagram.loads(s)
    assert d.dumps() == s[:-1]
    assert 'bar' in d.modules
    assert 'foo' in d.modules
    assert 'fred' in d.modules
    assert 'quux' in d.modules


def test_sequence_loop():
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
    d = SequenceDiagram.loads(s)
    assert d.dumps() == s[:-1]
    assert 'bar' in d.modules
    assert 'foo' in d.modules
    assert 'thud' in d.modules


def test_sequence_comment():
    s = '''# Sequence
title: Comment

# This is comment
foo -> bar:
  # This is comment too
'''
    d = SequenceDiagram.loads(s)
    assert d.dumps() == '''# Sequence
title: Comment

foo -> bar'''


def test_sequence_moduleattr_error():
    s = '''# Sequence
foo.invalid: Foo
'''
    with pytest.raises(BadAttribute) as e:
        SequenceDiagram.loads(s)
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 16
Invalid attribute: foo.invalid.\
'''


def test_sequence_moduleattr():
    s = '''# Sequence
title: Foo Bar

foo.title: Foo
foo.type: Actor
bar.title: Bar

foo -> bar: baz
'''
    d = SequenceDiagram.loads(s)
    assert d.dumps() == s[:-1]


def test_sequence_title_error():
    s = '''# Sequence
invalid: Foo Bar

foo -> bar: baz
'''
    with pytest.raises(BadAttribute) as e: d = SequenceDiagram.loads(s)
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 16
Invalid attribute: invalid.\
'''


def test_sequence_title():
    s = '''# Sequence
title: Foo Bar

foo -> bar: baz
'''
    d = SequenceDiagram.loads(s)
    assert d.dumps() == s[:-1]


def test_sequence_calltext():
    s = '''# Sequence
title: Foo Bar

foo -> bar: baz
foo -> bar: int baz.qux(quux):int
  bar -> baz: thud
    foo -> bar
      foo -> bar: 123 !@#$%^&*() {}[];',./?><"\\|
foo -> bar
'''
    d = SequenceDiagram.loads(s)
    assert d.dumps() == s[:-1]


def test_sequence_hierarchy():
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
    d = SequenceDiagram.loads(s)
    assert d.dumps() == s[:-1]


def test_interpreter_badsyntax():
    with pytest.raises(BadSyntax) as e:
        SequenceDiagram().feedline('foo')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 1, col 3
Expected one of `->|:|.`, got: NEWLINE.\
'''

    with pytest.raises(BadSyntax) as e:
        SequenceDiagram.loads('''
            foo
            bar
        ''')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 2, col 15
Expected one of `->|:|.`, got: NEWLINE.\
'''

    with pytest.raises(BadSyntax) as e:
        SequenceDiagram.loads('''
            title: Foo
              foo: bar
        ''')
    assert str(e.value) == '''\
File "String", Interpreter SequenceDiagram, line 3, col 17
Expected `->`, got: COLON ":".\
'''
