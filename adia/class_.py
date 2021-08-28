from io import StringIO

from .interpreter import Interpreter, GoTo, New, Terminate
from .token import EVERYTHING, NEWLINE, HASH, EOF, NAME
from .container import Container


class Class_(Interpreter):
    name = None

    def __init__(self, *args, **kw):
        super().__init__('start', *args, **kw)

    def _set_name(self, name):
        self.name = name

    def __repr__(self):
        return f'Class: {self.name}'

    def dumps(self):
        f = StringIO()
        f.write(self.name)

        return f.getvalue()

    statemap = {
        'start': {
            NAME: {NEWLINE: GoTo('attr', cb=_set_name)},
            NEWLINE: GoTo('start', ignore=True)
        },
        'attr': {
            NEWLINE: GoTo('attr', ignore=True),
            NAME: Terminate(reuse=True),
            EOF: Terminate(reuse=True),
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
        return f'ClassDiagram: {self.title}'

    def dumps(self):
        f = StringIO()
        f.write('class:')

        if self.title:
            f.write(f' {self.title}')

        f.write('\n')

        if len(self):
            f.write('\n')
            for c in self:
                f.write(c.dumps())
                f.write('\n')

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
