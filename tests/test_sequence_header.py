from adia import Diagram

from .helpers import eqdia


def test_sequence_header():
    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence: Bar
    ''')
    assert eqdia(d.renders(), '''
    .................
    . DIAGRAM: Foo  .
    . version: 1.0  .
    .               .
    .               .
    . SEQUENCE: Bar .
    .               .
    .................
    ''')

    d = Diagram('''
        diagram: Foo
        version: 1.0
        sequence:
    ''')
    assert eqdia(d.renders(), '''
    ................
    . DIAGRAM: Foo .
    . version: 1.0 .
    .              .
    ................
    ''')
