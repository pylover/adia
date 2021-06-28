import contextlib


@contextlib.contextmanager
def raises(extype):
    class ExceptionProxy:
        value = None

    p = ExceptionProxy()
    try:
        yield p
    except Exception as e:
        p.value = e
