from adia import Diagram

from .helpers import eqdia


def test_diagram_header():
    # Empty Input
    d = Diagram()
    assert eqdia(d, '''
    ........
    ........
    ''')

    # Version Only
    d = Diagram('''
        version: 1.0
    ''')
    assert eqdia(d, '''
    ................
    . version: 1.0 .
    ................
    ''')

    d = Diagram('''
        diagram: Foo
        version: 1.0
    ''')
    assert eqdia(d, '''
    ................
    . DIAGRAM: Foo .
    . version: 1.0 .
    ................
    ''')

    d = Diagram('''
        diagram: Foo
    ''')
    assert eqdia(d, '''
    ................
    . DIAGRAM: Foo .
    ................
    ''')

    d = Diagram('''
        diagram: Foo
        author: alice
    ''')
    assert eqdia(d, '''
    .................
    . DIAGRAM: Foo  .
    . author: alice .
    .................
    ''')

    d = Diagram('''
        diagram: Foo
        author: alice
        version: 1.0
    ''')
    assert eqdia(d, '''
    .................
    . DIAGRAM: Foo  .
    . author: alice .
    . version: 1.0  .
    .................
    ''')


def test_space_at_emptyline_issue46():
    d = Diagram('\n'.join((
        'diagram: Foo',
        '  ',
        '# foo'
    )))
    assert eqdia(d, '''
    ................
    . DIAGRAM: Foo .
    ................
    ''')
