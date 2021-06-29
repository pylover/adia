from dial.ascii import ASCIICanvas


NEWLINE = '↵\n'


def norm(s):
    return s.replace('\n', NEWLINE)


def eq(a, b):
    b = b.strip()

    bb = []
    for l in b.splitlines():
        bb.append(l[5:-1])

    bb.pop(0)
    bb.pop()
    bb[-1] += '\n'
    b = '\n'.join(bb)

    a += '\n'
    try:
        assert a == b
    except AssertionError:
        print('Given:')
        print(norm(a))
        print('Expected:')
        print(norm(b))
        raise ValueError()


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
    c = ASCIICanvas(11, 5)
    c.draw_box(3, 1, 5, 3)
    eq(str(c), '''\
    .............
    .           .
    .   +---+   .
    .   |   |   .
    .   +---+   .
    .           .
    .............
    ''')
