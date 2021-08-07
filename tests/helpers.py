import contextlib

from adia.diagram import Diagram


def eqbigstr(a, b, offset=8):
    if hasattr(a, 'dumps'):
        a = a.dumps()
    elif not isinstance(a, str):
        a = str(a)

    bb = []
    for line in b.splitlines():
        bb.append(line[offset:])

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


def eqdia(a, b, offset=4):

    def annotate(s):
        i = 0
        for line in s.splitlines():
            yield f'. {line} . {i:3d}\n'
            i += 1

    def maxwidth(*args):
        m = 0
        for s in args:
            linelen = [len(line) for line in s.splitlines()]
            if linelen:
                m = max(m, max(linelen))

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

        print(f'  {first}')
        print(f'  {second}')

    if isinstance(a, Diagram):
        a = a.renders(rstrip=False)

    bb = []
    for line in b.strip().splitlines():
        bb.append(line[offset + 2:-2])

    bb.pop(0)
    bb.pop()
    b = '\n'.join(bb)
    maxlen = maxwidth(a, b)
    maxanlen = maxlen + 4
    if a.endswith('\n'):
        b += '\n'

    if a != b:
        print('\nGiven:')
        print_columns(maxlen)
        print('.' * (maxanlen))
        print(''.join(annotate(a)), end='')
        print('.' * (maxanlen))
        print('\nExpected:')
        print_columns(maxlen)
        print('.' * (maxanlen))
        print(''.join(annotate(b)), end='')
        print('.' * (maxanlen))
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
