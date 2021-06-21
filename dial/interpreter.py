import abc

from .token import *
from .token import EXACT_TOKENS_DICT


class BadSyntax(Exception):
    def __init__(self, interpreter, token):
        got = TOKEN_NAMES[token.type]
        if token.string.strip():
            gotstr = f' "{token.string}"'
        else:
            gotstr = ''

        validtokens = [
            EXACT_TOKENS_DICT.get(i, TOKEN_NAMES[i])
            for i in interpreter.state.keys()
        ]
        if len(validtokens) > 1:
            expected = f'Expected one of `{"|".join(validtokens)}`'
        elif len(validtokens) == 1:
            expected = f'Expected `{validtokens[0]}`'

        filename = interpreter.filename or 'String'

        super().__init__(
            f'File "{filename}", line {token.start[0]}, col {token.start[1]}\n'
            f'{expected}, got: {got}{gotstr}.')


class Action:
    def __init__(self, nextstate=None):
        self.nextstate = nextstate

    def __call__(self, interpreter):
        return self.nextstate


class Ignore(Action):
    def __call__(self, interpreter):
        interpreter.tokenstack.clear()
        return super().__call__(interpreter)


class Hook(Action):
    def __init__(self, callback, nextstate=None):
        super().__init__(nextstate)
        self.callback = callback

    def __call__(self, interpreter):
        args = interpreter.tokenstack.copy()
        interpreter.tokenstack.clear()
        newstate = self.callback(interpreter, *args)

        return self.nextstate if self.nextstate else newstate


class Goto(Action):
    def __call__(self, interpreter):
        return self.nextstate


class Interpreter(metaclass=abc.ABCMeta):
    def __init__(self, tokenizer, initstate):
        self.tokenizer = tokenizer
        self.state = self.states[initstate]
        self.tokenstack = []
        self.filename = None

    def parseline(self, line):
        if len(line) and not line.endswith('\n'):
            line += '\n'

        for token in self.tokenizer.tokenizeline(line):
            self.perform(token)

    def parse(self, string):
        for token in self.tokenizer.tokenizes(string):
            self.perform(token)

    @property
    @abc.abstractmethod
    def states(self):
        raise NotImplementedError()

    def perform(self, token):
        backup = self.state
        try:
            self.state = self.state[token.type]
        except KeyError:
            raise BadSyntax(self, token)

        if token.type == NAME:
            self.tokenstack.append(token.string)

        if callable(self.state):
            newstate = self.state(self)

            if newstate is not None:
                self.state = self.states[newstate]
            else:
                self.state = backup
