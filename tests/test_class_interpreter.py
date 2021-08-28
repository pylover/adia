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
    '''
    eqrepr(s)
