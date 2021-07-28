from adia import Diagram

from .helpers import eqdia


def test_diagram_header():
    d = Diagram('''
        diagram: Foo
        version: 1.0
    ''')
    assert eqdia(d.renders(), '''
    ................
    . DIAGRAM: Foo .
    . version: 1.0 .
    .              .
    ................
    ''')

    d = Diagram()
    assert eqdia(d.renders(), '''
    .............................
    . DIAGRAM: Untitled Diagram .
    .                           .
    .............................
    ''')

    d = Diagram('''
        diagram: Foo
    ''')
    assert eqdia(d.renders(), '''
    ................
    . DIAGRAM: Foo .
    .              .
    ................
    ''')

    d = Diagram('''
        diagram: Foo
        author: alice
    ''')
    assert eqdia(d.renders(), '''
    .................
    . DIAGRAM: Foo  .
    . author: alice .
    .               .
    .................
    ''')

    d = Diagram('''
        diagram: Foo
        author: alice
        version: 1.0
    ''')
    assert eqdia(d.renders(), '''
    .................
    . DIAGRAM: Foo  .
    . author: alice .
    . version: 1.0  .
    .               .
    .................
    ''')
