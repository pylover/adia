from adia import Diagram

from .helpers import eqdia


def test_class_header():
    d = Diagram('''
        class: Foo
    ''')
    assert eqdia(d, '''
    ......................
    . CLASS DIAGRAM: Foo .
    ......................
    ''')


def test_class_single():
    d = Diagram('''
        class:
        foo
    ''')
    assert eqdia(d, '''
    ...........
    . +-----+ .
    . | foo | .
    . +-----+ .
    ...........
    ''')


def test_class_attr():
    d = Diagram('''
        class:
        foo
          bar
          baz
    ''')
    assert eqdia(d, '''
    ...........
    . +-----+ .
    . | foo | .
    . +-----+ .
    . | bar | .
    . | baz | .
    . +-----+ .
    ...........
    ''')


def test_class_position():
    d = Diagram('''
        class:
        foo
        bar
    ''')
    assert eqdia(d, '''
    ...................
    . +-----+ +-----+ .
    . | foo | | bar | .
    . +-----+ +-----+ .
    ...................
    ''')
