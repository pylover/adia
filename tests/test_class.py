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
          aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

        bar
          bbbbbbbbbbbbbb

        baz
        qux
        quux
        thud
          cccc
          dddd
    ''')
    assert eqdia(d, '''
    ....................................................................................
    . +-------------------------------------------+ +----------------+ +-----+ +-----+ .
    . | foo                                       | | bar            | | baz | | qux | .
    . +-------------------------------------------+ +----------------+ +-----+ +-----+ .
    . | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa | | bbbbbbbbbbbbbb |                 .
    . +-------------------------------------------+ +----------------+                 .
    . +------+ +------+                                                                .
    . | quux | | thud |                                                                .
    . +------+ +------+                                                                .
    .          | cccc |                                                                .
    .          | dddd |                                                                .
    .          +------+                                                                .
    ....................................................................................
    ''')  # noqa


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


def test_class_inheritance():
    d = Diagram('''
        class:
        foo(bar, baz)
    ''')
    assert eqdia(d, '''
    ...................
    . +-----+ +-----+ .
    . | bar | | baz | .
    . +-----+ +-----+ .
    .   ^        ^    .
    .   |        |    .
    .   | +------+    .
    .   | |           .
    . +-----+         .
    . | foo |         .
    . +-----+         .
    ...................
    ''')
    assert d[0][0].title == 'foo'
    assert d[0][1].title == 'bar'
    assert d[0][2].title == 'baz'


# def test_class_ref():
#     d = Diagram('''
#         class:
#         foo
#           b -> bar
#     ''')
#     assert eqdia(d, '''
#     ...................
#     . +-----+ +-----+ .
#     . | foo | | bar | .
#     . +-----+ +-----+ .
#     . | b   |         .
#     . +-----+         .
#     ...................
#     ''')
#     assert d[0][0].title == 'foo'
#     assert d[0][1].title == 'bar'


# Inheritance
# Reference
# Self reference
