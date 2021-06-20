import abc

from .token import *


class BadSyntax(Exception):
    def __init__(self, interpreter, token):
        validtokens = [TOKEN_NAMES[i] for i in interpreter.state.keys()]
        got = TOKEN_NAMES[token.type]
        if token.string.strip():
            gotstr = f' "{token.string}"'
        else:
            gotstr = ''

        if len(validtokens) > 1:
            expected = f'Expected one of: ({"|".join(validtokens)})'
        elif len(validtokens) == 1:
            expected = f'Expected: {validtokens[0]}'

        filename = interpreter.filename or 'String'

        super().__init__(
            f'File "{filename}", line {token.start[0]}\n'
            f'{expected}, got: {got}{gotstr}.')


class Action(metaclass=abc.ABCMeta):
    def __init__(self, nextstate):
        self.nextstate = nextstate

    @abc.abstractmethod
    def __call__(self, interpreter):
        raise NotImplementedError()


class Callback(Action):
    def __init__(self, callback, nextstate):
        self.callback = callback
        super().__init__(nextstate)

    def __call__(self, interpreter):
        self.callback(interpreter, *interpreter.tokenstack)
        interpreter.tokenstack.clear()
        return self.nextstate


class Ignore(Action):
    def __call__(self, interpreter):
        interpreter.tokenstack.clear()
        return self.nextstate


class Interpreter(metaclass=abc.ABCMeta):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.state = self.states['root']
        self.tokenstack = []
        self.filename = None

    def parseline(self, line):
        if len(line) and not line.endswith('\n'):
            line += '\n'

        for token in self.tokenizer.tokenizeline(line):
            self.perform(token)

    @property
    @abc.abstractmethod
    def states(self):
        raise NotImplementedError()

    def perform(self, token):
        try:
            self.state = self.state[token.type]
        except KeyError:
            raise BadSyntax(self, token)

        if token.type == NAME:
            self.tokenstack.append(token.string)

        if isinstance(self.state, Action):
            self.state = self.states[self.state(self)]
