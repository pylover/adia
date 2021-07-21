from io import StringIO

from dial import Diagram

from .helpers import eqdia


def test_render_string():
    d = Diagram('''
    diagram: My dia
    sequence:

    foo -> bar
    ''')

    assert eqdia(d.renders(), '''
    ...................
    . DIAGRAM: My dia .
    .                 .
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
    .                 .
    ...................
    ''')


def test_render_file():
    d = Diagram('''
    diagram: My dia
    sequence:

    foo -> bar
    ''')

    f = StringIO()
    d.render(f)
    assert eqdia(f.getvalue(), '''
    ...................
    . DIAGRAM: My dia .
    .                 .
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
    .                 .
    ..
    ...................
    ''')
