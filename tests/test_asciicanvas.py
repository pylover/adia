from dial.ascii import ASCIICanvas

from .helpers import eq


def test_asciicanvas_drawline():
    c = ASCIICanvas(8, 5)
    c.draw_vline(1, 1, 2)
    eq(str(c), '''\
    ..........
    .        .
    . |      .
    . |      .
    .        .
    .        .
    ..........
    ''')

    c.draw_hline(1, 3, 4)
    eq(str(c), '''\
    ..........
    .        .
    . |      .
    . |      .
    . ----   .
    .        .
    ..........
    ''')


def test_asciicanvas_drawbox():
    c = ASCIICanvas(11, 6)
    c.draw_box(3, 1, 5, 4)
    eq(str(c), '''\
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
    c = ASCIICanvas(11, 3)
    c.draw_textline(3, 1, 'foo')
    eq(str(c), '''\
    .............
    .           .
    .   foo     .
    .           .
    .............
    ''')


def test_asciicanvas_drawtextblock():
    c = ASCIICanvas(11, 5)
    c.draw_textblock(3, 1, 'foo\n\n  bar')
    eq(str(c), '''\
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
    eq(str(c), '''\
    .............
    .           .
    .  +-----+  .
    .  |foo  |  .
    .  |     |  .
    .  |  bar|  .
    .  +-----+  .
    .............
    ''')

    c = ASCIICanvas(14, 6)
    c.draw_textbox(2, 1, 'foo\n\n  bar', hmargin=1)
    eq(str(c), '''\
    ................
    .              .
    .  +-------+   .
    .  | foo   |   .
    .  |       |   .
    .  |   bar |   .
    .  +-------+   .
    ................
    ''')

    c = ASCIICanvas(14, 8)
    c.draw_textbox(2, 1, 'foo\n\n  bar', hmargin=1, vmargin=1)
    eq(str(c), '''\
    ................
    .              .
    .  +-------+   .
    .  |       |   .
    .  | foo   |   .
    .  |       |   .
    .  |   bar |   .
    .  |       |   .
    .  +-------+   .
    ................
    ''')


def test_asciicanvas_drawarrow():
    c = ASCIICanvas(12, 5)
    c.draw_rightarrow(4, 1, 4)
    c.draw_leftarrow(4, 3, 4)
    c.draw_toparrow(2, 1, 3)
    c.draw_bottomarrow(9, 1, 3)
    eq(str(c), '''\
    ..............
    .            .
    .  ^ ---> |  .
    .  |      |  .
    .  | <--- v  .
    .            .
    ..............
    ''')
