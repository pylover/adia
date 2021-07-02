import contextlib


def eqbigstr(a, b):
    if hasattr(a, 'dumps'):
        a = a.dumps()
    elif not isinstance(a, str):
        a = str(a)

    bb = []
    for l in b.splitlines():
        bb.append(l[8:])

    b = '\n'.join(bb[1:-1])

    if a.endswith('\n'):
        b += '\n'

    if a != b:
        print('######################## Given:')
        print(a)
        print('######################## Expected:')
        print(b)
        print('########################')
        return False

    return True


def eqdia(a, b):
    NEWLINE = '↵'

    def annotate(s):
        i = 0
        for l in s.splitlines():
            yield f'{l}{NEWLINE} {i:3d}\n'
            i += 1

    def maxwidth(*args):
        m = 0
        for s in args:
            ll = [len(l) for l in s.splitlines()]
            if ll:
                m = max(m, max(ll))

        return m

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

    maxlen = maxwidth(a, b) + 2
    b = b.strip()

    bb = []
    for l in b.splitlines():
        bb.append(l[5:-1])

    bb.pop(0)
    bb.pop()
    bb[-1] += '\n'
    b = '\n'.join(bb)

    a += '\n'
    if a != b:
        print('Given:')
        print_columns(maxlen)
        print(''.join(annotate(a)))
        print('Expected:')
        print_columns(maxlen)
        print(''.join(annotate(b)))
        return False

    return True


@contextlib.contextmanager
def raises(exttype):
    class ExceptionProxy:
        value = None

    p = ExceptionProxy()
    try:
        yield p
    except Exception as e:
        if not isinstance(e, exttype):
            raise

        # Allow pytest count asserts
        assert isinstance(e, exttype)
        p.value = e
