class LazyAttribute:
    """A decorator to freeze the property value.

    This decorator is intended to promote a
    function call to object attribute. This means the
    function is called once and replaced with
    returned value.

    >>> class A:
    ...     def __init__(self):
    ...         self.counter = 0
    ...     @LazyAttribute
    ...     def count(self):
    ...         self.counter += 1
    ...         return self.counter
    >>> a = A()
    >>> a.count
    1
    >>> a.count
    1
    """

    __slots__ = ('f', )

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, t=None):
        f = self.f
        if obj is None:
            return f
        val = f(obj)
        setattr(obj, f.__name__, val)
        return val
