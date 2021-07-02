from dial.ascii import ASCIIRenderer
from dial.diagram import Diagram

from .helpers import eqdia


def test_asciidiagram_header():
    r = ASCIIRenderer(Diagram('''
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

    r = ASCIIRenderer(Diagram())
    assert eqdia(str(r.render()), '''
    .............................
    . DIAGRAM: Untitled Diagram .
    .                           .
    .............................
    ''')

    r = ASCIIRenderer(Diagram('''
        diagram: Foo
    '''))
    assert eqdia(str(r.render()), '''
    ................
    . DIAGRAM: Foo .
    .              .
    ................
    ''')

    r = ASCIIRenderer(Diagram('''
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

    r = ASCIIRenderer(Diagram('''
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
