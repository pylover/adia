from dial.canvas import Canvas

from .helpers import eqdia


def test_canvas_extend():
    c = Canvas()
    assert c.size == (0, 0)
    c.extendright(1)
    c.extendbottom(3)
    assert c.size == (1, 3)

    c.draw_vline(0, 0, 3)
    assert eqdia(str(c), '''
    .....
    . | .
    . | .
    . | .
    .....
    ''')

    c.extendright(2)
    assert c.size == (3, 3)
    assert eqdia(str(c), '''
    .......
    . |   .
    . |   .
    . |   .
    .......
    ''')

    c.extendleft(2)
    assert c.size == (5, 3)
    assert eqdia(str(c), '''
    .........
    .   |   .
    .   |   .
    .   |   .
    .........
    ''')

    c.extendtop(1)
    assert c.size == (5, 4)
    assert eqdia(str(c), '''
    .........
    .       .
    .   |   .
    .   |   .
    .   |   .
    .........
    ''')

    c.extendbottom(1)
    assert c.size == (5, 5)
    assert eqdia(str(c), '''
    .........
    .       .
    .   |   .
    .   |   .
    .   |   .
    .       .
    .........
    ''')


def test_canvas_write_hcenter():
    c = Canvas()
    c.write_hcenter(0, 0, 'Foo Bar Baz')
    assert eqdia(str(c), '''
    ...............
    . Foo Bar Baz .
    ...............
    ''')


def test_canvas_drawline():
    c = Canvas()
    c.draw_vline(3, 1, 3)
    assert eqdia(str(c), '''
    ........
    .      .
    .    | .
    .    | .
    .    | .
    ........
    ''')

    c.draw_hline(1, 2, 5)
    assert eqdia(str(c), '''
    ..........
    .        .
    .    |   .
    .  ----- .
    .    |   .
    ..........
    ''')


def test_canvas_drawbox():
    c = Canvas()
    c.draw_box(3, 1, 5, 4)
    assert eqdia(str(c), '''
    ............
    .          .
    .    +---+ .
    .    |   | .
    .    |   | .
    .    +---+ .
    ............
    ''')


def test_canvas_drawtextline():
    c = Canvas()
    c.write_textline(3, 1, 'foo')
    assert eqdia(str(c), '''
    ..........
    .        .
    .    foo .
    ..........
    ''')


def test_canvas_drawtextblock():
    c = Canvas()
    c.write_textblock(3, 1, 'foo\n\n  bar')
    assert eqdia(str(c), '''
    ............
    .          .
    .    foo   .
    .          .
    .      bar .
    ............
    ''')


def test_canvas_drawtextbox():
    c = Canvas()
    c.draw_textbox(1, 1, 'foo')
    assert eqdia(str(c), '''
    ..........
    .        .
    .  +---+ .
    .  |foo| .
    .  +---+ .
    ..........
    ''')

    c = Canvas()
    c.draw_textbox(1, 1, 'foo', hpadding=(1, 2))
    assert eqdia(str(c), '''
    .............
    .           .
    .  +------+ .
    .  | foo  | .
    .  +------+ .
    .............
    ''')

    c = Canvas()
    c.draw_textbox(2, 1, 'foo\n\n  bar')
    assert eqdia(str(c), '''
    .............
    .           .
    .   +-----+ .
    .   |foo  | .
    .   |     | .
    .   |  bar| .
    .   +-----+ .
    .............
    ''')

    c = Canvas()
    c.draw_textbox(3, 1, 'foo\n\n  bar', hpadding=1)
    assert eqdia(str(c), '''
    ................
    .              .
    .    +-------+ .
    .    | foo   | .
    .    |       | .
    .    |   bar | .
    .    +-------+ .
    ................
    ''')

    c = Canvas()
    c.draw_textbox(3, 1, 'foo\n\n  bar', hpadding=1, vpadding=1)
    assert eqdia(str(c), '''
    ................
    .              .
    .    +-------+ .
    .    |       | .
    .    | foo   | .
    .    |       | .
    .    |   bar | .
    .    |       | .
    .    +-------+ .
    ................
    ''')


def test_canvas_drawarrow():
    c = Canvas()
    c.draw_rightarrow(4, 2, 12)
    c.draw_leftarrow(4, 6, 12)
    c.draw_toparrow(2, 2, 5)
    c.draw_bottomarrow(17, 2, 5)
    assert eqdia(str(c), '''
    ......................
    .                    .
    .                    .
    .   ^ -----------> | .
    .   |              | .
    .   |              | .
    .   |              | .
    .   | <----------- v .
    ......................
    ''')


def test_canvas_drawarrowtext():
    c = Canvas()
    c.draw_rightarrow(4, 2, 12, texttop='foo', text='bar', textbottom='thud')
    c.draw_leftarrow(5, 6, 10, texttop='foo', text='bar', textbottom='thud')
    c.draw_toparrow(2, 2, 5)
    c.draw_bottomarrow(17, 2, 5)
    assert eqdia(str(c), '''
    ......................
    .                    .
    .         foo        .
    .   ^ ----bar----> | .
    .   |    thud      | .
    .   |              | .
    .   |      foo     | .
    .   |  <---bar---  v .
    .         thud       .
    ......................
    ''')
