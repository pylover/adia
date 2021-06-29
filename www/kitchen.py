class Foo(list):
    def __init__(self, *args, **kw):
        print(args, kw)
        super().__init__(*args, **kw)


def run():
    s = Foo()
    print(s)


# Brython
# CPython
