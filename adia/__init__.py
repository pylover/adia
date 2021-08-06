"""ADia language parser and ASCII renderer.

:class:`Diagram` is a collection of actual diagrams such as
:class:`SequenceDiagram`.

:class:`Diagram` implements the :class:`Interpreter` abstract class and uses
:class:`Tokenizer` and :class:`Renderer` internally to do it's job.

"""


from .diagram import Diagram
from .exceptions import InterpreterError, BadAttribute, BadSyntax
from .renderer import Renderer


__version__ = '0.1.1'


def renders(source):
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
    :return: ASCII diagram.
    :rtype: str
    """
    return Diagram(source).renders()


def render(source, out):
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
    """
    Diagram(source).render(out)
