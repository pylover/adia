from io import StringIO

from dial.exceptions import BadAttribute
from dial.diagram import Diagram

from .helpers import raises, eqbigstr


def test_diagram_full():
    diagram = Diagram()
    s = '''
        diagram: Foo
        version: 1.0
        author: thud

        sequence: Bar Baz

        # Modules
        bar.title: Bar
        foo.type: Actor

        foo -> bar
          bar -> baz: init()
    '''

    diagram <<= StringIO(s)
    assert eqbigstr(diagram.dumps(), s)


def test_diagram_comment():
    s = '''
        diagram: Foo
        # This is Comment
    '''
    assert eqbigstr(Diagram.loads(s).dumps(), '''
        diagram: Foo
    ''')


def test_diagram_repr():
    diagram = Diagram()
    assert repr(diagram) == 'Diagram: Untitled Diagram'

    diagram <<= 'diagram: Foo'
    assert repr(diagram) == 'Diagram: Foo'


def test_diagram_attr_error():
    s = '''
        diagram: Foo
        invalid: invalid
    '''
    with raises(BadAttribute) as e:
        Diagram.loads(s)
    assert eqbigstr(e.value, '''
        File "String", Interpreter Diagram, line 3, col 24
        Invalid attribute: invalid.
    ''')
