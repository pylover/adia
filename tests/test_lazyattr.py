from dial.lazyattr import LazyAttribute


def test_lazyattribute():
    global callcount

    class MyType:
        pass
    my_instance = MyType()

    callcount = 0

    class Foo:
        @LazyAttribute
        def bar(self):
            """Foo bar baz."""
            global callcount
            callcount += 1
            return my_instance

    assert 'Foo bar baz.' == Foo.bar.__doc__
    assert 'bar' == Foo.bar.__name__

    foo = Foo()
    assert my_instance is foo.bar
    assert 1 == callcount
