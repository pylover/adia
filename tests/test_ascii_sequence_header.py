from dial.ascii import ASCIIRenderer
from dial.diagram import Diagram

from .helpers import eqdia


def test_asciisequence_header():
    r = ASCIIRenderer(Diagram('''
        diagram: Foo
        version: 1.0
        sequence: Bar
    '''))
    assert eqdia(r.dumps(), '''
    .................
    . DIAGRAM: Foo  .
    . version: 1.0  .
    .               .
    . SEQUENCE: Bar .
    .               .
    .................
    ''')

    r = ASCIIRenderer(Diagram('''
        diagram: Foo
        version: 1.0
        sequence:
    '''))
    assert eqdia(r.dumps(), '''
    ................
    . DIAGRAM: Foo .
    . version: 1.0 .
    .              .
    ................
    ''')
