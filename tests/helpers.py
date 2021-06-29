import contextlib


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
