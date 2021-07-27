from io import StringIO

from .container import Container
from .interpreter import Interpreter, Ignore, Switch, Goto, Consume, New
from .sequence import SequenceDiagram
from .token import *
from .renderer import Renderer


class Diagram(Interpreter, Container):
    title = 'Untitled Diagram'
    version = None
    author = None

    def __init__(self, initial=None, *args, **kwargs):
        super().__init__('start', *args, **kwargs)
        if initial is None:
            return

        if isinstance(initial, str):
            self.parse(initial)
        else:
            self.parsefile(initial)

    def __repr__(self):
        return f'Diagram: {self.title}'

    def dumps(self):
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

        return f.getvalue()

    def parsefile(self, f):
        if hasattr(f, 'name'):
            self.tokenizer.filename = f.name

        while True:
            line = f.readline()
            self.parseline(line)
            if not line:
                return

    def parseline(self, line):
        if len(line) and not line.endswith('\n'):
            line += '\n'

        for token in self.tokenizer.feedline(line):
            self.eat_token(token)

        return

    def parse(self, string):
        with StringIO(string) as f:
            self.parsefile(f)

    def render(self, filelike):
        Renderer(self).dump(filelike)

    def renders(self):
        return Renderer(self).dumps()

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
