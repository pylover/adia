from dial.exceptions import BadSyntax, BadAttribute
from dial.sequence import SequenceDiagram
from dial import Diagram

from .helpers import raises, eqbigstr


def seq(s):
    d = Diagram(s)
    assert len(d) == 1
    assert isinstance(d[0], SequenceDiagram)
    return d[0]


def eqrepr(s):
    assert eqbigstr(seq(s), s)


def test_sequence_note_errors():
    with raises(BadSyntax) as e:
        seq('''
            sequence: foo
            @~:
        ''')
    assert eqbigstr(e.value, '''
        BadSyntax: File "String", Interpreter: SequenceDiagram, line 3, col 13
        Expected `NAME`, got: `~`.
    ''')

    with raises(BadSyntax) as e:
        seq('''
            sequence: foo
            @foo bar
        ''')
    assert eqbigstr(e.value, '''
        BadSyntax: File "String", Interpreter: Note, line 3, col 17
        Expected one of `~ :`, got: `bar`.
    ''')

    with raises(BadSyntax) as e:
        seq('''
            sequence: foo
            @foo ~ bar ~
        ''')
    assert eqbigstr(e.value, '''
        BadSyntax: File "String", Interpreter: Note, line 3, col 23
        Expected `:`, got: `~`.
    ''')


def test_sequence_noteover():
    s = '''
        sequence: note over

        @foo: over Foo.
        @foo ~ bar: from Foo to the Bar
        @foo ~ baz: |
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore.

        foo -> bar
          @foo: Over Foo
    '''
    d = seq(s)
    assert eqbigstr(d, s)
    assert 'foo' in d.modules
    assert 'bar' in d.modules
    assert 'baz' in d.modules
    assert list(d[0].modules) == ['foo']
    assert list(d[1].modules) == ['foo', 'bar']
    assert list(d[2].modules) == ['foo', 'baz']
    assert list(d[3][0].modules) == ['foo']


def test_sequenceitem_repr():
    d = seq('''
        sequence: foo
        foo -> bar
        foo -> bar:
        foo -> bar: baz
        for: i in range(10)
          foo -> baz
    ''')
    assert repr(d[0]) == 'SequenceItem: foo -> bar'
    assert repr(d[1]) == 'SequenceItem: foo -> bar'
    assert repr(d[2]) == 'SequenceItem: foo -> bar'
    assert repr(d[3]) == 'SequenceItem: for'


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
        BadAttribute: File "String", Interpreter: SequenceDiagram, line 3, col 24
        Invalid attribute: foo.invalid.
    ''')  # noqa


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
        BadAttribute: File "String", Interpreter: SequenceDiagram, line 3, col 24
        Invalid attribute: invalid.
    ''')  # noqa


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
        BadSyntax: File "String", Interpreter: SequenceDiagram, line 2, col 3
        Expected one of `-> : .`, got: `NEWLINE`.
    ''')

    with raises(BadSyntax) as e:
        seq('sequence: foo\n@')
    assert eqbigstr(e.value, '''
        BadSyntax: File "String", Interpreter: SequenceDiagram, line 2, col 1
        Expected `NAME`, got: `NEWLINE`.
    ''')

    with raises(BadSyntax) as e:
        seq('''
            sequence: foo
              foo:')
        ''')
    assert eqbigstr(e.value, '''
        BadSyntax: File "String", Interpreter: SequenceDiagram, line 3, col 17
        Expected `->`, got: `:`.
    ''')


def test_sequence_returntext():
    s = '''
        sequence:

        foo -> bar: hello() -> hi
    '''
    d = seq(s)
    assert eqbigstr(d, s)
    assert d[0].returntext == 'hi'
