"""Lazy attributes module."""


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

    __slots__ = ('_factory', )

    def __init__(self, factory):
        self._factory = factory

    def __get__(self, obj, owner=None):
        factory = self._factory
        if obj is None:
            return factory
        val = factory(obj)
        setattr(obj, factory.__name__, val)
        return val
