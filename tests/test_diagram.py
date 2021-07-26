from dial import Diagram

from .helpers import eqdia


def test_diagram_break_issue9():
    d = Diagram('''
        diagram: Foo
        version: 1.0

        sequence: Foo #1
        foo -> bar

        sequence: Foo #2
        foo -> bar
    ''')
    assert eqdia(d.renders(), '''
    ....................
    . DIAGRAM: Foo     .
    . version: 1.0     .
    .                  .
    .                  .
    . SEQUENCE: Foo #1 .
    .                  .
    . +-----+ +-----+  .
    . | foo | | bar |  .
    . +-----+ +-----+  .
    .    |       |     .
    .    |~~~~~~>|     .
    .    |       |     .
    .    |<------|     .
    .    |       |     .
    . +-----+ +-----+  .
    . | foo | | bar |  .
    . +-----+ +-----+  .
    .                  .
    .                  .
    . SEQUENCE: Foo #2 .
    .                  .
    . +-----+ +-----+  .
    . | foo | | bar |  .
    . +-----+ +-----+  .
    .    |       |     .
    .    |~~~~~~>|     .
    .    |       |     .
    .    |<------|     .
    .    |       |     .
    . +-----+ +-----+  .
    . | foo | | bar |  .
    . +-----+ +-----+  .
    .                  .
    ....................
    ''')
