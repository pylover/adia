from dial.exceptions import BadSyntax, BadAttribute
from dial.sequence import SequenceDiagram
from dial.diagram import Diagram

from .helpers import raises, eqbigstr


def seq(s):
    d = Diagram.loads(s)
    assert len(d) == 1
    assert isinstance(d[0], SequenceDiagram)
    return d[0]


def eqrepr(s):
    assert eqbigstr(seq(s), s)


def test_sequence_note():
    s = '''
        sequence: note

        @over: |
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore.

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
    d = seq(s)
    assert eqbigstr(d, s)
    assert 'thud' in d.modules
    assert 'bar' in d.modules
    assert 'baz' in d.modules
    assert 'foo' in d.modules
    assert 'qux' in d.modules
    assert 'quux' in d.modules


def test_sequenceitem_repr():
    d = seq('''
        sequence: foo
        foo -> bar
        foo -> bar:
        foo -> bar: baz
        for: i in range(10)
          foo -> baz
    ''')
    assert repr(d[0]) == 'foo -> bar'
    assert repr(d[1]) == 'foo -> bar'
    assert repr(d[2]) == 'foo -> bar: baz'
    assert repr(d[3]) == 'for: i in range(10)'


def test_sequence_repr():
    d = seq('sequence: foo')
    assert repr(d) == 'SequenceDiagram: foo'


def test_sequence_condition():
    s = '''
        sequence: condition

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
    d = seq(s)
    assert eqbigstr(d, s)
    assert 'bar' in d.modules
    assert 'foo' in d.modules
    assert 'fred' in d.modules
    assert 'quux' in d.modules


def test_sequence_loop():
    s = '''
        sequence: loop

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
    d = seq(s)
    assert eqbigstr(d, s)
    assert 'bar' in d.modules
    assert 'foo' in d.modules
    assert 'thud' in d.modules


def test_sequence_comment():
    s = '''
        sequence: Comment

        # This is comment
        foo -> bar:
          # This is comment too
    '''
    assert eqbigstr(seq(s), '''# Sequence
        sequence: Comment

        foo -> bar
    ''')


def test_sequence_moduleattr_error():
    s = '''
        sequence: error
        foo.invalid: Foo
    '''
    with raises(BadAttribute) as e:
        seq(s)
    assert eqbigstr(e.value, '''
        File "String", Interpreter SequenceDiagram, line 3, col 24
        Invalid attribute: foo.invalid.
    ''')


def test_sequence_moduleattr():
    eqrepr('''
        sequence: Foo Bar

        # Modules
        bar.title: Bar
        foo.title: Foo
        foo.type: Actor

        foo -> bar: baz
    ''')


def test_sequence_title_error():
    s = '''
        sequence: Foo Bar
        invalid: Foo Bar

        foo -> bar: baz
    '''
    with raises(BadAttribute) as e:
        seq(s)

    assert eqbigstr(e.value, '''
        File "String", Interpreter SequenceDiagram, line 3, col 24
        Invalid attribute: invalid.
    ''')


def test_sequence_title():
    eqrepr('''
        sequence: Foo Bar

        foo -> bar: baz
    ''')


def test_sequence_calltext():
    eqrepr('''
        sequence: Foo Bar

        foo -> bar: baz
        foo -> bar: int baz.qux(quux):int
          bar -> baz: thud
            foo -> bar
              foo -> bar: 123 !@#$%^&*() {}[];',./?><"\\|
        foo -> bar
    ''')


def test_sequence_hierarchy():
    eqrepr('''
        sequence: Foo Bar

        foo -> bar
        foo -> baz
          baz -> qux
            qux -> bar
              qux -> bar
            qux -> bar
          baz -> qux
        foo -> bar
    ''')


def test_sequence_attrs():
    eqrepr('''
        sequence: Foo Bar
    ''')

    eqrepr('''
        sequence: Foo Bar
        description: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        tags: foo bar baz

        # Modules
        foo.type: Actor

        foo -> bar
    ''')

    eqrepr('''
        sequence: Foo Bar
        description: Lorem ipsum dolor sit amet, consectetur adipiscing elit.

        foo -> bar
    ''')

    eqrepr('''
        sequence: Foo Bar
        tags: foo bar baz

        foo -> bar
    ''')

    eqrepr('''
        sequence: Foo Bar
        tags: foo bar baz
    ''')


def test_interpreter_badsyntax():
    with raises(BadSyntax) as e:
        seq('sequence: foo\nfoo')
    assert eqbigstr(e.value, '''
        File "String", Interpreter SequenceDiagram, line 2, col 3
        Expected one of `->|:|.`, got: NEWLINE.
    ''')

    with raises(BadSyntax) as e:
        seq('sequence: foo\n@')
    assert eqbigstr(e.value, '''
        File "String", Interpreter SequenceDiagram, line 2, col 1
        Expected `NAME`, got: NEWLINE.
    ''')

    with raises(BadSyntax) as e:
        seq('''
            sequence: foo
              foo:')
        ''')
    assert eqbigstr(e.value, '''
        File "String", Interpreter SequenceDiagram, line 3, col 17
        Expected `->`, got: COLON ":".
    ''')
