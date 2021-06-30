from io import StringIO

from .container import Container
from .interpreter import Interpreter, Ignore, Switch, Goto, Consume, New
from .sequence import SequenceDiagram
from .token import *


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

    def _set_title(self, attr, value):
        self.title = value.strip()

    def _attr(self, attr, value):
        value = value.strip()

        if attr == 'version':
            self.version = value
        elif attr == 'author':
            self.author = value
        else:
            raise AttributeError(attr)

    def _new_seq(self, sequence):
        self.append(sequence)

    _keywords = {
        'diagram': Goto(nextstate='title'),
        'sequence': New(SequenceDiagram, callback=_new_seq, nextstate='start'),
    }

    statemap = {
        'start': {
            HASH: {EVERYTHING: {NEWLINE: Ignore(nextstate='start')}},
            NEWLINE: Ignore(nextstate='start'),
            EOF: Ignore(nextstate='start'),
            NAME: Switch(default=Goto(nextstate='name'), **_keywords),
        },
        'title': {
            COLON: {EVERYTHING: {
                NEWLINE: Consume(_set_title, nextstate='start')
            }}
        },
        'name': {
            COLON: Goto(nextstate='attr:'),
        },
        'attr:': {
            EVERYTHING: {NEWLINE: Consume(_attr, nextstate='start')}
        },
    }
