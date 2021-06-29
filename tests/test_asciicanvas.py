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

    c.draw_hline(3, 1, 4)
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


def test_asciicanvas_drawtext():
    c = ASCIICanvas(11, 5)
    c.draw_text(3, 1, 'foo\n\n  bar')
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
