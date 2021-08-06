"""The :mod:`adia` module makes it easy to get ``ASCII`` diagrams using
:func:`render` and :func:`renders`.

In addition, :class:`Diagram` class may be used to access the low-level API.
"""

from .diagram import Diagram
from .sequence import SequenceDiagram
from .exceptions import InterpreterError, BadAttribute, BadSyntax
from .renderer import Renderer


__version__ = '0.1.1'


def renders(source, rstrip=True):
    """High level API to generate ASCII diagram.

    Equivalent to:

    .. code-block:: python

       Diagram(source).renders()

    Example:

    .. code-block:: python

       import adia

       print(adia.renders('''
           diagram: Foo
           sequence:
           foo -> bar: Hello World!
       '''))

    :param source: The ADia source code.
    :type source: str or file-like
    :param rstrip: If ``True``, the trailing wihtespaces at the end of each
                   line will be removed.
    :type rstrip: bool, optional, default: True
    :return: ASCII diagram.
    :rtype: str
    """
    return Diagram(source).renders(rstrip)


def render(source, out, rstrip=True):
    """High level API to write ASCII diagram into file.

    Equivalent to:

    .. code-block:: python

       Diagram(source).render(out)

    Example:

    .. code-block:: python

       import adia

       source = '''
          diagram: Foo
          sequence:
          foo -> bar: Hello World!
      ''''
       with open('foo.txt', 'w') as outfile:
           adia.render(source, otfile)

    :param source: The ADia source code.
    :type source: str or file-like
    :param rstrip: If ``True``, the trailing wihtespaces at the end of each
                   line will be removed.
    :type rstrip: bool, optional, default: True
    """
    Diagram(source).render(out, rstrip)
