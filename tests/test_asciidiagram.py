from dial.ascii import ASCIIDiagramRenderer
from dial.diagram import Diagram

from .helpers import eqdia


def test_asciidiagram_header():
    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
        version: 1.0
    '''))
    assert eqdia(str(r.render()), '''
    ................
    . DIAGRAM: Foo .
    . version: 1.0 .
    .              .
    ................
    ''')

    r = ASCIIDiagramRenderer(Diagram())
    assert eqdia(str(r.render()), '''
    .............................
    . DIAGRAM: Untitled Diagram .
    .                           .
    .............................
    ''')

    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
    '''))
    assert eqdia(str(r.render()), '''
    ................
    . DIAGRAM: Foo .
    .              .
    ................
    ''')

    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
        author: alice
    '''))
    assert eqdia(str(r.render()), '''
    .................
    . DIAGRAM: Foo  .
    . author: alice .
    .               .
    .................
    ''')

    r = ASCIIDiagramRenderer(Diagram('''
        diagram: Foo
        author: alice
        version: 1.0
    '''))
    assert eqdia(str(r.render()), '''
    .................
    . DIAGRAM: Foo  .
    . author: alice .
    . version: 1.0  .
    .               .
    .................
    ''')
