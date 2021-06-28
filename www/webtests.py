from contextlib import contextmanager


@contextmanager
def ctx():
    yield 'hello'


def run():
    print('Running Dial web tests')
