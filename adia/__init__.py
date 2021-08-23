"""``ASCII`` diagrams language parser and renderer.
:func:`print` and :func:`diagram`.

In addition, :class:`Diagram` class may be used to access the low-level API.
"""
import sys

from .diagram import Diagram
from .sequence import SequenceDiagram
from .exceptions import InterpreterError, BadAttribute, BadSyntax
from .renderer import Renderer


__version__ = '4.0.4'
__all__ = [
    'Diagram',
    'SequenceDiagram',
    'InterpreterError',
    'BadAttribute',
    'BadSyntax',
    'Renderer',
    'print',
    'diagram'
]


def diagram(source, rstrip=True):
    """High level API to generate ASCII diagram.

    This function is equivalent to:

    .. code-block:: python

       Diagram(source).renders()

    :param source: The ADia source code.
    :type source: str or file-like
    :param rstrip: If ``True``, the trailing wihtespaces at the end of each
                   line will be removed.
    :type rstrip: bool, optional, default: True
    :return: ASCII diagram.
    :rtype: str

    """
    return Diagram(source).renders(rstrip)


def print(source, file=None, rstrip=True):
    """High level API to write ASCII diagram into file.

    Equivalent to:

    .. code-block:: python

       Diagram(source).render(file)

    Example

    .. code-block:: python

       import adia

       source = '''
          diagram: Foo
          sequence:
          foo -> bar: Hello World!
      ''''
       with open('foo.txt', 'w') as outfile:
           adia.print(source, file=outfile)

    :param source: The ADia source code.
    :type source: str or file-like
    :param file: An object with the ``write`` attribute. If ``None`` the
                 :attr:`sys.stdout` will be used instead.
    :param rstrip: If ``True``, the trailing wihtespaces at the end of each
                   line will be removed.
    :type rstrip: bool, optional, default: True

    """
    Diagram(source).render(file or sys.stdout, rstrip)
