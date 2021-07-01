from dial.ascii import ASCIIRenderer
from dial.diagram import Diagram

from .helpers import eqdia


def test_asciidiagram_header():
    r = ASCIIRenderer(Diagram())
    eqdia(str(r.render()), '''
    ..................
    .Untitled Diagram.
    .                .
    ..................
    ''')

    r = ASCIIRenderer(Diagram('''
        diagram: Foo
    '''))
    eqdia(str(r.render()), '''
    .....
    .Foo.
    .   .
    .....
    ''')

    r = ASCIIRenderer(Diagram('''
        diagram: Foo
        version: 1.0
    '''))
    eqdia(str(r.render()), '''
    ..............
    .Foo         .
    .            .
    .version: 1.0.
    .            .
    ..............
    ''')

    r = ASCIIRenderer(Diagram('''
        diagram: Foo
        author: alice
    '''))
    eqdia(str(r.render()), '''
    ...............
    .Foo          .
    .             .
    .author: alice.
    .             .
    ...............
    ''')

    r = ASCIIRenderer(Diagram('''
        diagram: Foo
        author: alice
        version: 1.0
    '''))
    eqdia(str(r.render()), '''
    ...............
    .Foo          .
    .             .
    .author: alice.
    .version: 1.0 .
    .             .
    ...............
    ''')
