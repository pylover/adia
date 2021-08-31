from adia.class_ import ClassDiagram
from adia import Diagram

from .helpers import eqbigstr


def class_(s):
    d = Diagram(s)
    assert len(d) == 1
    assert isinstance(d[0], ClassDiagram)
    return d[0]


def eqrepr(s):
    assert eqbigstr(class_(s), s)


def test_class_minimal():
    s = '''
        class:

        foo
        bar
        baz
    '''
    eqrepr(s)


def test_class_title():
    s = '''
        class: Foo

        foo
    '''
    eqrepr(s)


def test_class_repr():
    c = class_('''
        class:
    ''')
    assert repr(c) == 'ClassDiagram: Untitled'

    c = class_('''
        class: Foo
    ''')
    assert repr(c) == 'ClassDiagram: Foo'

    c = class_('''
        class: Foo
        foo
    ''')
    assert repr(c[0]) == 'Class: foo'


def test_class_simple_attribute():
    s = '''
        class: Foo

        foo
          bar
          baz

        Foo
          Bar
          Baz
    '''
    eqrepr(s)


def test_class_multiwords_attribute():
    s = '''
        class: Foo

        foo
          bar baz
          +baz

        Foo
          Bar Baz
          Baz Qux
    '''
    eqrepr(s)


def test_class_method():
    s = '''
        class: Foo

        foo
          int bar(a, *b, c)
          *Bar bar(int *a)
    '''
    eqrepr(s)


def test_class_reference():
    s = '''
        class: Foo

        foo
          bar -> baz
    '''
    eqrepr(s)

    d = class_('''
        class: Foo
        foo
          bar -> baz
    ''')
    assert len(d) == 1


def test_class_inheritance():
    s = '''
        class: Foo

        foo(bar)
          int bar(a, *b, c)
          *Bar bar(int *a)

        bar(baz, qux)
    '''
    eqrepr(s)
