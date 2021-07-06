from io import StringIO

from dial import Diagram, ASCIIRenderer

from .helpers import eqdia


def test_lowlevel_api():
    d = Diagram('''
    diagram: My dia
    sequence:

    foo -> bar
    ''')

    r = ASCIIRenderer(d)
    assert eqdia(r.dumps(), '''
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


def test_lowlevel_api_file():
    d = Diagram('''
    diagram: My dia
    sequence:

    foo -> bar
    ''')

    r = ASCIIRenderer(d)
    f = StringIO()
    r.dump(f)
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
