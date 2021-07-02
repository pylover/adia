from dial.ascii import ASCIICanvas

from .helpers import eqdia


def test_asciicanvas_extend():
    c = ASCIICanvas()
    assert c.size == (0, 0)
    c.extendright(1)
    c.extendbottom(3)
    assert c.size == (1, 3)

    c.draw_vline(0, 0, 3)
    assert eqdia(str(c), '''
    ...
    .|.
    .|.
    .|.
    ...
    ''')

    c.extendright(2)
    assert c.size == (3, 3)
    assert eqdia(str(c), '''
    .....
    .|  .
    .|  .
    .|  .
    .....
    ''')

    c.extendleft(2)
    assert c.size == (5, 3)
    assert eqdia(str(c), '''
    .......
    .  |  .
    .  |  .
    .  |  .
    .......
    ''')

    c.extendtop(1)
    assert c.size == (5, 4)
    assert eqdia(str(c), '''
    .......
    .     .
    .  |  .
    .  |  .
    .  |  .
    .......
    ''')

    c.extendbottom(1)
    assert c.size == (5, 5)
    assert eqdia(str(c), '''
    .......
    .     .
    .  |  .
    .  |  .
    .  |  .
    .     .
    .......
    ''')


def test_asciicanvas_write_hcenter():
    c = ASCIICanvas()
    c.write_hcenter(0, 0, 'Foo Bar Baz')
    assert eqdia(str(c), '''
    .............
    .Foo Bar Baz.
    .............
    ''')


def test_asciicanvas_drawline():
    c = ASCIICanvas()
    c.draw_vline(3, 1, 3)
    assert eqdia(str(c), '''
    ......
    .    .
    .   |.
    .   |.
    .   |.
    ......
    ''')

    c.draw_hline(1, 2, 5)
    assert eqdia(str(c), '''
    ........
    .      .
    .   |  .
    . -----.
    .   |  .
    ........
    ''')


def test_asciicanvas_drawbox():
    c = ASCIICanvas()
    c.draw_box(3, 1, 5, 4)
    assert eqdia(str(c), '''
    ..........
    .        .
    .   +---+.
    .   |   |.
    .   |   |.
    .   +---+.
    ..........
    ''')


def test_asciicanvas_drawtextline():
    c = ASCIICanvas()
    c.write_textline(3, 1, 'foo')
    assert eqdia(str(c), '''
    ........
    .      .
    .   foo.
    ........
    ''')


def test_asciicanvas_drawtextblock():
    c = ASCIICanvas()
    c.write_textblock(3, 1, 'foo\n\n  bar')
    assert eqdia(str(c), '''
    ..........
    .        .
    .   foo  .
    .        .
    .     bar.
    ..........
    ''')


def test_asciicanvas_drawtextbox():
    c = ASCIICanvas()
    c.draw_textbox(2, 1, 'foo\n\n  bar')
    assert eqdia(str(c), '''
    ...........
    .         .
    .  +-----+.
    .  |foo  |.
    .  |     |.
    .  |  bar|.
    .  +-----+.
    ...........
    ''')

    c = ASCIICanvas()
    c.draw_textbox(3, 1, 'foo\n\n  bar', hmargin=1)
    assert eqdia(str(c), '''
    ..............
    .            .
    .   +-------+.
    .   | foo   |.
    .   |       |.
    .   |   bar |.
    .   +-------+.
    ..............
    ''')

    c = ASCIICanvas()
    c.draw_textbox(3, 1, 'foo\n\n  bar', hmargin=1, vmargin=1)
    assert eqdia(str(c), '''
    ..............
    .            .
    .   +-------+.
    .   |       |.
    .   | foo   |.
    .   |       |.
    .   |   bar |.
    .   |       |.
    .   +-------+.
    ..............
    ''')


def test_asciicanvas_drawarrow():
    c = ASCIICanvas()
    c.draw_rightarrow(4, 2, 12)
    c.draw_leftarrow(4, 6, 12)
    c.draw_toparrow(2, 2, 5)
    c.draw_bottomarrow(17, 2, 5)
    assert eqdia(str(c), '''
    ....................
    .                  .
    .                  .
    .  ^ -----------> |.
    .  |              |.
    .  |              |.
    .  |              |.
    .  | <----------- v.
    ....................
    ''')


def test_asciicanvas_drawarrowtext():
    c = ASCIICanvas()
    c.draw_rightarrow(4, 2, 12, texttop='foo', text='bar', textbottom='baz')
    c.draw_leftarrow(5, 6, 10, texttop='foo', text='bar', textbottom='baz')
    c.draw_toparrow(2, 2, 5)
    c.draw_bottomarrow(17, 2, 5)
    assert eqdia(str(c), '''
    ....................
    .                  .
    .        foo       .
    .  ^ ----bar----> |.
    .  |     baz      |.
    .  |              |.
    .  |      foo     |.
    .  |  <---bar---  v.
    .         baz      .
    ....................
    ''')
