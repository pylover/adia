from dial.ascii import ASCIICanvas

from .helpers import eqdia


def test_asciicanvas_drawline():
    c = ASCIICanvas(7, 5)
    c.draw_vline(3, 1, 3)
    eqdia(str(c), '''
    .........
    .       .
    .   |   .
    .   |   .
    .   |   .
    .       .
    .........
    ''')

    c.draw_hline(1, 2, 5)
    eqdia(str(c), '''
    .........
    .       .
    .   |   .
    . ----- .
    .   |   .
    .       .
    .........
    ''')


def test_asciicanvas_drawbox():
    c = ASCIICanvas(11, 6)
    c.draw_box(3, 1, 5, 4)
    eqdia(str(c), '''
    .............
    .           .
    .   +---+   .
    .   |   |   .
    .   |   |   .
    .   +---+   .
    .           .
    .............
    ''')


def test_asciicanvas_drawtextline():
    c = ASCIICanvas(9, 3)
    c.write_textline(3, 1, 'foo')
    eqdia(str(c), '''
    ...........
    .         .
    .   foo   .
    .         .
    ...........
    ''')


def test_asciicanvas_drawtextblock():
    c = ASCIICanvas(11, 5)
    c.write_textblock(3, 1, 'foo\n\n  bar')
    eqdia(str(c), '''
    .............
    .           .
    .   foo     .
    .           .
    .     bar   .
    .           .
    .............
    ''')


def test_asciicanvas_drawtextbox():
    c = ASCIICanvas(11, 6)
    c.draw_textbox(2, 1, 'foo\n\n  bar')
    eqdia(str(c), '''
    .............
    .           .
    .  +-----+  .
    .  |foo  |  .
    .  |     |  .
    .  |  bar|  .
    .  +-----+  .
    .............
    ''')

    c = ASCIICanvas(15, 6)
    c.draw_textbox(3, 1, 'foo\n\n  bar', hmargin=1)
    eqdia(str(c), '''
    .................
    .               .
    .   +-------+   .
    .   | foo   |   .
    .   |       |   .
    .   |   bar |   .
    .   +-------+   .
    .................
    ''')

    c = ASCIICanvas(15, 8)
    c.draw_textbox(3, 1, 'foo\n\n  bar', hmargin=1, vmargin=1)
    eqdia(str(c), '''
    .................
    .               .
    .   +-------+   .
    .   |       |   .
    .   | foo   |   .
    .   |       |   .
    .   |   bar |   .
    .   |       |   .
    .   +-------+   .
    .................
    ''')


def test_asciicanvas_drawarrow():
    c = ASCIICanvas(20, 9)
    c.draw_rightarrow(4, 2, 12)
    c.draw_leftarrow(4, 6, 12)
    c.draw_toparrow(2, 2, 5)
    c.draw_bottomarrow(17, 2, 5)
    eqdia(str(c), '''
    ......................
    .                    .
    .                    .
    .  ^ -----------> |  .
    .  |              |  .
    .  |              |  .
    .  |              |  .
    .  | <----------- v  .
    .                    .
    .                    .
    ......................
    ''')


def test_asciicanvas_drawarrowtext():
    c = ASCIICanvas(20, 9)
    c.draw_rightarrow(4, 2, 12, texttop='foo', text='bar', textbottom='baz')
    c.draw_leftarrow(5, 6, 10, texttop='foo', text='bar', textbottom='baz')
    c.draw_toparrow(2, 2, 5)
    c.draw_bottomarrow(17, 2, 5)
    eqdia(str(c), '''
    ......................
    .                    .
    .        foo         .
    .  ^ ----bar----> |  .
    .  |     baz      |  .
    .  |              |  .
    .  |      foo     |  .
    .  |  <---bar---  v  .
    .         baz        .
    .                    .
    ......................
    ''')
