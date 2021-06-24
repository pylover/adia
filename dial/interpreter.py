import abc

from .token import *
from .token import EXACT_TOKENS_DICT


class InterpreterError(Exception):
    def __init__(self, interpreter, token, msg):
        filename = interpreter.tokenizer.filename or 'String'

        super().__init__(
            f'File "{filename}", '
            f'Interpreter {interpreter.__class__.__name__}, '
            f'line {token.start[0]}, col {token.start[1]}\n'
            f'{msg}'
        )


class BadAttribute(InterpreterError):
    def __init__(self, interpreter, token, attr):
        super().__init__(interpreter, token, f'Invalid attribute: {attr}.')


class BadSyntax(InterpreterError):
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

        super().__init__(
            interpreter, token, f'{expected}, got: {got}{gotstr}.'
        )


class Action:
    def __init__(self, nextstate=None):
        self.nextstate = nextstate

    def __call__(self, interpreter, token):
        return self.nextstate


class Goto(Action):
    def __init__(self, callback=None, nextstate=None):
        self.callback = callback
        super().__init__(nextstate)

    def __call__(self, interpreter, token):
        if self.callback:
            self.callback(interpreter)

        return super().__call__(interpreter, token)


class Consume(Action):
    capture = [
        NAME,
        EVERYTHING,
        MULTILINE,
    ]

    def __init__(self, callback=None, nextstate=None):
        self.callback = callback
        super().__init__(nextstate)

    def _call_callback(self, interpreter, token, *args, **kw):
        if self.callback is None:
            return

        try:
            self.callback(interpreter, *args, **kw)
        except AttributeError as e:
            raise BadAttribute(interpreter, token, '.'.join(e.args))

    def __call__(self, interpreter, token):
        args = tuple(
            i.string for i in interpreter.tokenstack if i.type in self.capture
        )
        interpreter.tokenstack.clear()
        self._call_callback(interpreter, token, *args)

        return super().__call__(interpreter, token)


class Ignore(Consume):
    def __call__(self, interpreter, token):
        interpreter.tokenstack.clear()
        return super().__call__(interpreter, token)


class FinalConsume(Consume):
    def __init__(self, callback):
        super().__init__(callback, None)

    def __call__(self, interpreter, token):
        interpreter.more = False
        super().__call__(interpreter, token)


class New(Consume):
    target = None
    parent = None

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        super().__init__(*args, **kwargs)

    def __call__(self, parent, token):
        self.target = self.factory(parent.tokenizer)
        self.parent = parent

        while parent.tokenstack:
            self.eat_token(parent.tokenstack.pop(0))

        return self

    def eat_token(self, token):
        more = self.target.eat_token(token)
        if more:
            return None

        self._call_callback(self.parent, token, self.target)

        return self.nextstate


class Interpreter(metaclass=abc.ABCMeta):
    def __init__(self, tokenizer, initialstate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tokenizer = tokenizer
        self.more = True
        self.state = self.statemap[initialstate]
        self.tokenstack = []

    @property
    @abc.abstractmethod
    def statemap(self):
        raise NotImplementedError()

    def _set_state(self, key):
        if isinstance(key, str):
            self.state = self.statemap[key]
        else:
            self.state = key

    def _redirect(self, target, token):
        newstatekey = target.eat_token(token)
        if newstatekey:
            self._set_state(newstatekey)

    def eat_token(self, token):
        if isinstance(self.state, New):
            return self._redirect(self.state, token)

        try:
            newstate = self.state[token.type]
        except KeyError:
            raise BadSyntax(self, token)

        self.tokenstack.append(token)

        if callable(newstate):
            newstate = newstate(self, token)

        self._set_state(newstate)
        return self.more

    def parseline(self, line):
        if len(line) and not line.endswith('\n'):
            line += '\n'

        for token in self.tokenizer.tokenizeline(line):
            self.eat_token(token)

    def parse(self, string):
        for token in self.tokenizer.tokenizes(string):
            self.eat_token(token)
