from dial import Diagram

from .helpers import eqdia


def test_readme_quickstart():
    d = Diagram('''
        diagram: Foo

        sequence:

        foo -> bar: Hello World!

    ''')
    assert eqdia(d.renders(), '''
    ...............................
    . DIAGRAM: Foo                .
    .                             .
    . +-----+             +-----+ .
    . | foo |             | bar | .
    . +-----+             +-----+ .
    .    |                   |    .
    .    |~~~Hello World!~~~>|    .
    .    |                   |    .
    .    |<------------------|    .
    .    |                   |    .
    . +-----+             +-----+ .
    . | foo |             | bar | .
    . +-----+             +-----+ .
    .                             .
    ...............................
    ''')
