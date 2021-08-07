from io import StringIO

from adia import Diagram, renders, print as adiaprint

from .helpers import eqdia


def test_render_string():
    d = Diagram('''
    diagram: My dia
    sequence:

    foo -> bar
    ''')

    assert eqdia(d, '''
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
    ...................
    ''')


def test_render_file():
    d = Diagram('''
    diagram: My dia
    sequence:

    foo -> bar
    ''')

    f = StringIO()
    d.render(f, rstrip=False)
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
    ...................
    ''')


def test_renders_function():
    out = renders('''
    diagram: My dia
    sequence:

    foo -> bar
    ''', rstrip=False)

    assert eqdia(out, '''
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
    ...................
    ''')

    out = renders('''
    diagram: My dia
    sequence:

    foo -> bar
    ''', rstrip=True)

    assert eqdia(out, '''
    ...................
    . DIAGRAM: My dia .
    .  .
    . +-----+ +-----+ .
    . | foo | | bar | .
    . +-----+ +-----+ .
    .    |       | .
    .    |~~~~~~>| .
    .    |       | .
    .    |<------| .
    .    |       | .
    . +-----+ +-----+ .
    . | foo | | bar | .
    . +-----+ +-----+ .
    ...................
    ''')


def test_print_function():
    out = StringIO()
    adiaprint('''
    diagram: My dia
    sequence:

    foo -> bar
    ''', out, rstrip=False)

    assert eqdia(out.getvalue(), '''
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
    ...................
    ''')

    out = StringIO()
    adiaprint('''
    diagram: My dia
    sequence:

    foo -> bar
    ''', out, rstrip=True)

    assert eqdia(out.getvalue(), '''
    ...................
    . DIAGRAM: My dia .
    .  .
    . +-----+ +-----+ .
    . | foo | | bar | .
    . +-----+ +-----+ .
    .    |       | .
    .    |~~~~~~>| .
    .    |       | .
    .    |<------| .
    .    |       | .
    . +-----+ +-----+ .
    . | foo | | bar | .
    . +-----+ +-----+ .
    ...................
    ''')
