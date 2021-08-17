import abc

from .token import TOKEN_NAMES, EXACT_TOKENS_DICT, MULTILINE, EVERYTHING, \
    NAME
from .tokenizer import Tokenizer
from .exceptions import BadSyntax, BadAttribute


class Action:
    def __init__(self, nextstate=None):
        self.nextstate = nextstate

    def __call__(self, interpreter, token):
        return self.nextstate


class Switch(Action):
    def __init__(self, default=None, **kw):
        self.default = default
        self.cases = {k.rstrip('_'): v for k, v in kw.items()}
        super().__init__()

    def __call__(self, interpreter, token, *args):
        action = self.cases.get(token.string, self.default)
        if action is None:
            raise BadSyntax(interpreter, token, expected=self.cases.keys())

        return action(interpreter, token, *args)


class Goto(Action):
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

    def __call__(self, interpreter, token, *args):
        self._call_callback(interpreter, token, *args)
        return super().__call__(interpreter, token)


class Consume(Goto):
    limit = [
        NAME,
        EVERYTHING,
        MULTILINE,
    ]

    def __init__(self, callback=None, nextstate=None, alltokens=False):
        if alltokens:
            self.limit = None

        super().__init__(callback=callback, nextstate=nextstate)

    def __call__(self, interpreter, token, *args):
        args = tuple(
            i.string for i in interpreter.tokenstack if
            not self.limit or i.type in self.limit
        )
        interpreter.tokenstack.clear()
        return super().__call__(interpreter, token, *args)


class Ignore(Consume):
    def __call__(self, interpreter, token):
        interpreter.tokenstack.clear()
        return super().__call__(interpreter, token)


class Final(Action):
    def __call__(self, interpreter, *args, **kw):
        interpreter.more = False
        return super().__call__(interpreter, *args, **kw)


class FinalConsume(Consume):
    def __call__(self, interpreter, *args, **kw):
        interpreter.more = False
        return super().__call__(interpreter, *args, **kw)


class New(Consume):
    target = None
    parent = None

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        super().__init__(*args, **kwargs)

    def __call__(self, parent, token):
        self.target = self.factory(tokenizer=parent.tokenizer)
        self.parent = parent

        while parent.tokenstack:
            self.eat_token(parent.tokenstack.pop(0))

        return self

    def eat_token(self, token):
        more, nextstate = self.target.eat_token(token)
        if more:
            return None

        self._call_callback(self.parent, token, self.target)

        return self.nextstate or nextstate


class Interpreter(metaclass=abc.ABCMeta):
    def __init__(self, initialstate, *args, tokenizer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tokenizer = tokenizer if tokenizer else Tokenizer()
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
        if newstatekey is not None:
            self._set_state(newstatekey)

    def eat_token(self, token):
        if isinstance(self.state, New):
            self._redirect(self.state, token)
            return self.more, None

        try:
            newstate = self.state[token.type]
        except KeyError:
            validtokens = [
                EXACT_TOKENS_DICT.get(i, TOKEN_NAMES[i])
                for i in self.state.keys()
            ]
            raise BadSyntax(self, token, expected=validtokens)

        self.tokenstack.append(token)

        if callable(newstate):
            newstate = newstate(self, token)

        if not self.more:
            return self.more, newstate

        self._set_state(newstate)
        return True, None
