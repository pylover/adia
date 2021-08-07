from io import StringIO

from .container import Container
from .interpreter import Interpreter, Ignore, Switch, Goto, Consume, New
from .sequence import SequenceDiagram
from .token import NEWLINE, NAME, EVERYTHING, INDENT, EOF, HASH, COLON
from .renderer import Renderer


class Diagram(Interpreter, Container):
    """The main entrypoint of the :mod:`adia` package.

    :class:`Diagram` is a collection of actual diagrams such as
    :class:`SequenceDiagram` which implements the :class:`Interpreter`
    abstract class and uses :class:`Tokenizer` and :class:`Renderer`
    internally to do it's job.

    :param source: ADia source code to parse.
    :type source: str or file-like

    .. note::

       You may use the :meth:`dumps` method to dump back the diagram instance
       to ``ADia`` source code.
    """
    title = 'Untitled Diagram'
    version = None
    author = None

    def __init__(self, source=None, *args, **kwargs):
        super().__init__('start', *args, **kwargs)
        if source is None:
            return

        if isinstance(source, str):
            self.parse(source)
        else:
            self.parsefile(source)

    def __repr__(self):
        return f'Diagram: {self.title}'

    def dumps(self):
        """Serialize back the diagram class into valid ``ADia`` source code.

        .. testsetup:: diagram

           from adia import Diagram

        .. testcode:: diagram

           diagram = Diagram('''
               diagram: Foo
               sequence:
               foo -> bar: Hello World!
           ''')

           print(diagram.dumps())

        .. testoutput:: diagram

           diagram: Foo

           sequence:

           foo -> bar: Hello World!

        """

        f = StringIO()
        f.write(f'diagram: {self.title}\n')

        if self.version:
            f.write(f'version: {self.version}\n')

        if self.author:
            f.write(f'author: {self.author}\n')

        if len(self):
            f.write('\n')
            for c in self:
                f.write(f'{c.dumps()}')

        return f.getvalue()[:-1]

    def parse(self, source):
        """Parses ``Adia`` source string.

        :param source: The ADia source code.
        :type source: str
        """
        with StringIO(source) as f:
            self.parsefile(f)

    def parsefile(self, sourcefile):
        """Parses an ``ADia`` source file into the current instance.

        :param sourcefile: The ADia source file.
        :type sourcefile: file-like object
        """
        if hasattr(sourcefile, 'name'):
            self.tokenizer.filename = sourcefile.name

        while True:
            line = sourcefile.readline()
            self.parseline(line)
            if not line:
                return

    def parseline(self, line):
        """Parse an ``ADia`` source line into the current instance.

        :param line:
        :type line: str
        """
        if len(line) and not line.endswith('\n'):
            line += '\n'

        for token in self.tokenizer.feedline(line):
            self.eat_token(token)

        return

    def render(self, outfile, rstrip=True):
        """Writes the ASCII represetation of the current instance into the
        outfile.

        :param outfile: An object with ``write(...)`` method.
        :param rstrip: If ``True``, the trailing wihtespaces at the end of each
                       line will be removed.
        :type rstrip: bool, optional, default: True
        """
        Renderer(self).dump(outfile, rstrip)

    def renders(self, rstrip=True):
        """Gets the ASCII represetation of the current instance.

        :param rstrip: If ``True``, the trailing wihtespaces at the end of each
                       line will be removed.
        :type rstrip: bool, optional, default: True
        :return: ASCII diagram.
        :rtype: str
        """
        return Renderer(self).dumps(rstrip)

    def _set_title(self, attr, value):
        self.title = value.strip()

    def _attr(self, attr, value):
        value = value.strip()

        if attr == 'version':
            self.version = value
        elif attr == 'author':
            self.author = value

    def _new_seq(self, sequence):
        self.append(sequence)

    _keywords = {
        'diagram': Goto(nextstate='title'),
        'author': Goto(nextstate='attr'),
        'version': Goto(nextstate='attr'),
        'sequence': Goto(nextstate='sequence'),
    }

    statemap = {
        'start': {
            HASH: {EVERYTHING: {NEWLINE: Ignore(nextstate='start')}},
            INDENT: {NEWLINE: Ignore(nextstate='start')},
            NEWLINE: Ignore(nextstate='start'),
            EOF: Ignore(nextstate='start'),
            NAME: Switch(**_keywords),
        },
        'title': {
            COLON: {EVERYTHING: {
                NEWLINE: Consume(_set_title, nextstate='start')
            }}
        },
        'attr': {
            COLON: {
                EVERYTHING: {NEWLINE: Consume(_attr, nextstate='start')}
            },
        },
        'sequence': {COLON: Ignore(nextstate='new-sequence')},
        'new-sequence': {
            EVERYTHING: {
                NEWLINE: New(
                    SequenceDiagram,
                    callback=_new_seq,
                )
            }
        }
    }
