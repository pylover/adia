from io import StringIO

from .container import Container
from .interpreter import Interpreter, GoTo, New, Switch
from .sequence import SequenceDiagram
from .class_ import ClassDiagram
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
    title = None
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
        if self.title:
            return f'Diagram: {self.title}'
        else:
            return 'Diagram: Untitled'

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
        br = False
        if self.title:
            f.write(f'diagram: {self.title}\n')
            br = True

        if self.version:
            f.write(f'version: {self.version}\n')
            br = True

        if self.author:
            f.write(f'author: {self.author}\n')
            br = True

        if len(self):
            if br:
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

    def _set_title(self, value):
        self.title = value.strip()

    def _attr(self, attr, value):
        value = value.strip()

        if attr == 'version':
            self.version = value
        elif attr == 'author':
            self.author = value

    def _new_seq(self, sequence):
        self.append(sequence)

    def _new_class(self, class_):
        self.append(class_)

    _keywords = {
        'diagram': GoTo('title', ignore=True),
        'author': GoTo('attr'),
        'version': GoTo('attr'),
        'sequence': GoTo('sequence'),
        'class': GoTo('class'),
    }

    statemap = {
        'start': {
            HASH: {EVERYTHING: {NEWLINE: GoTo('start', ignore=True)}},
            INDENT: {NEWLINE: GoTo('start', ignore=True)},
            NEWLINE: GoTo('start', ignore=True),
            EOF: GoTo('start', ignore=True),
            NAME: Switch(**_keywords),
        },
        'title': {
            COLON: {EVERYTHING: {
                NEWLINE: GoTo('start', cb=_set_title)
            }}
        },
        'attr': {
            COLON: {
                EVERYTHING: {NEWLINE: GoTo('start', cb=_attr)}
            },
        },
        'sequence': {COLON: GoTo('new-sequence', ignore=True)},
        'new-sequence': {EVERYTHING: {NEWLINE: New(
            SequenceDiagram,
            'start',
            cb=_new_seq
        )}},
        'class': {COLON: GoTo('new-class', ignore=True)},
        'new-class': {EVERYTHING: {NEWLINE: New(
            ClassDiagram,
            'start',
            cb=_new_class
        )}},
    }
