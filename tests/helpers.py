import contextlib


NEWLINE = '↵'


def annotate(s):
    i = 0
    for l in s.splitlines():
        yield f'{l}{NEWLINE} {i:3d}\n'
        i += 1


def maxwidth(*args):
    m = 0
    for s in args:
        m = max(m, max(len(l) for l in s.splitlines()))

    return m - 5


def print_columns(size):
    first, second = '', ''
    for i in range(size):
        j = i % 10
        if j == 0:
            first += f'{i // 10}'
        else:
            first += ' '
        second += f'{j}'

    print(first)
    print(second)


def eq(a, b):
    maxlen = maxwidth(a, b)
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
        print_columns(maxlen)
        print(''.join(annotate(a)))
        print('Expected:')
        print_columns(maxlen)
        print(''.join(annotate(b)))
        raise ValueError()


@contextlib.contextmanager
def raises(extype):
    class ExceptionProxy:
        value = None

    p = ExceptionProxy()
    try:
        yield p
    except Exception as e:
        assert isinstance(e, extype)
        p.value = e
