"""Another language for diagrams."""


from .diagram import Diagram
from .exceptions import InterpreterError
from .renderer import Renderer


__version__ = '0.1.1'


def renders(source):
    return Diagram(source).renders()


def render(source, out):
    Diagram(source).render(out)
