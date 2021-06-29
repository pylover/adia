import contextlib


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
