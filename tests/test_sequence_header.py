from adia import Diagram

from .helpers import eqdia


def test_sequence_header():
    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence: Bar
    ''')
    assert eqdia(d, '''
    .................
    . DIAGRAM: Foo  .
    . version: 1.0  .
    .               .
    .               .
    . SEQUENCE: Bar .
    .................
    ''')

    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence:
    ''')
    assert eqdia(d, '''
    ................
    . DIAGRAM: Foo .
    . version: 1.0 .
    ................
    ''')

    d = Diagram('''
        sequence: Foo
    ''')
    assert eqdia(d, '''
    .................
    . SEQUENCE: Foo .
    .................
    ''')

    d = Diagram('''
        sequence:
    ''')
    assert eqdia(d, '''
    ................
    ................
    ''')

    d = Diagram('''
        sequence:
        foo -> bar
    ''')
    assert eqdia(d, '''
    ...................
    . +-----+ +-----+ .
    . | foo | | bar | .
    . +-----+ +-----+ .
    .    |       |    .
    .    |~~~~~~>|    .
    .    |       |    .
    .    |<------|    .
    .    |       |    .
    . +-----+ +-----+ .
    . | foo | | bar | .
    . +-----+ +-----+ .
    ...................
    ''')
