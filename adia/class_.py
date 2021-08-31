import re
from io import StringIO

from .interpreter import Interpreter, GoTo, New, Terminate
from .token import EVERYTHING, NEWLINE, HASH, EOF, NAME, INDENT, DEDENT, \
    LPAR, RPAR, COMMA, ASTERISK, PLUS, MINUS, RARROW
from .container import Container


SPACEAFTER = re.compile(r'[a-z*]', re.I)
NOSPACEAFTER = re.compile(r'[)(*+-]')


class Attr:
    def __init__(self, text, ref=None):
        self.text = text
        self.ref = ref

    @classmethod
    def parse(cls, *args):
        ref = None
        f = StringIO()
        prev = None

        for i, a in enumerate(args[:-1]):
            if a == '->':
                ref = '.'.join(args[i + 1: -1])
                break
            if i > 0 \
                    and SPACEAFTER.match(a[0]) \
                    and not NOSPACEAFTER.match(prev[-1]):
                f.write(' ')
            f.write(a)
            prev = a

        return cls(f.getvalue(), ref)

    def dumps(self):
        parts = [self.text]

        if self.ref is not None:
            parts.extend(['->', self.ref])

        return ' '.join(parts)


class Class_(Interpreter):
    title = None

    def __init__(self, *args, **kw):
        self.members = []
        super().__init__('start', *args, **kw)

    def _set_name(self, title):
        self.title = title

    def __repr__(self):
        return f'Class: {self.title}'

    def dumps(self):
        f = StringIO()
        f.write(self.title)

        if self.members:
            f.write('\n')

            for attr in self.members:
                f.write(f'  {attr.dumps()}\n')

        return f.getvalue()

    def _new_attr(self, *args):
        attr = Attr.parse(*args)
        self.members.append(attr)

    statemap = {
        'start': {
            NAME: {NEWLINE: GoTo('  attr', cb=_set_name)},
            NEWLINE: GoTo('start', ignore=True)
        },
        '  attr': {
            NEWLINE: GoTo('  attr', ignore=True),
            NAME: Terminate(reuse=True),
            EOF: Terminate(reuse=True),
            INDENT: GoTo('attr', ignore=True),
        },
        'attr': {
            DEDENT: GoTo('  attr', ignore=True),
            NEWLINE: GoTo('attr', cb=_new_attr, limit=None),
            NAME: GoTo('attr', limit=None),
            LPAR: GoTo('attr', limit=None),
            RPAR: GoTo('attr', limit=None),
            COMMA: GoTo('attr', limit=None),
            ASTERISK: GoTo('attr', limit=None),
            PLUS: GoTo('attr', limit=None),
            MINUS: GoTo('attr', limit=None),
            RARROW: GoTo('attr', limit=None),
        }
    }


class ClassDiagram(Interpreter, Container):
    """Represents a class diagram.

    The :class:`adia.diagram` class creates an instance of this class for each
    class diagram section.

    """
    title = None

    def __init__(self, *args, **kwargs):
        super().__init__('title', *args, **kwargs)

    def __repr__(self):
        return f'ClassDiagram: {self.title or "Untitled"}'

    def dumps(self):
        f = StringIO()
        f.write('class:')

        if self.title:
            f.write(f' {self.title}')

        f.write('\n')

        if len(self):
            for c in self:
                f.write('\n')
                f.write(c.dumps())

        return f.getvalue()

    def _set_title(self, value, *args):
        self.title = value.strip()

    def _new_class(self, class_):
        self.append(class_)

    statemap = {
        'title': {
            EVERYTHING: {
                NEWLINE: GoTo('start', cb=_set_title)
            }
        },
        'start': {
            HASH: {EVERYTHING: {NEWLINE: GoTo('start', ignore=True)}},
            NEWLINE: GoTo('start', ignore=True),
            EOF: Terminate(),
            NAME: New(Class_, 'start', cb=_new_class)
        }
    }
