from dial.ascii import ASCIIDiagramRenderer
from dial.diagram import Diagram

from .helpers import eqdia


def test_asciisequence_header():
    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
        version: 1.0
        sequence: Bar
    '''))
    assert eqdia(str(r.render()), '''
    .................
    . DIAGRAM: Foo  .
    . version: 1.0  .
    .               .
    . SEQUENCE: Bar .
    .               .
    .................
    ''')

    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
        version: 1.0
        sequence:
    '''))
    assert eqdia(str(r.render()), '''
    ................
    . DIAGRAM: Foo .
    . version: 1.0 .
    .              .
    ................
    ''')
