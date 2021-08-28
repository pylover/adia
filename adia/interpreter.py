import abc

from .token import TOKEN_NAMES, EXACT_TOKENS_DICT, MULTILINE, EVERYTHING, \
    NAME
from .tokenizer import Tokenizer
from .exceptions import BadSyntax, BadAttribute


class Action(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, interpreter, token):
        pass


class GoTo(Action):
    def __init__(self, nextstate, cb=None, ignore=False, reuse=False,
                 limit=(NAME, EVERYTHING, MULTILINE)):
        self.nextstate = nextstate
        self.callback = cb
        self.ignore = ignore
        self.limit = limit
        self.reuse = reuse

    def _call_callback(self, interpreter, token):
        args = [i.string for i in interpreter.tokenstack]

        try:
            self.callback(interpreter, *args)
            interpreter.tokenstack.clear()
        except AttributeError as e:
            raise BadAttribute(interpreter, token, '.'.join(e.args))

    def __call__(self, interpreter, token):
        if self.ignore:
            interpreter.tokenstack.clear()
        else:
            interpreter.tokenstack.append(token)

        if self.limit:
            interpreter.tokenstack = [
                i for i in interpreter.tokenstack
                if i.type in self.limit
            ]

        if self.callback is not None:
            self._call_callback(interpreter, token)

        return self.nextstate, self.reuse


class New(GoTo):
    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        super().__init__(*args, **kwargs)

    def __call__(self, parent, token):
        if parent.redirect is None:
            parent.redirect = self.factory(tokenizer=parent.tokenizer)

            while parent.tokenstack:
                # Return values (more, reuse) are not needed here,
                # Because we can ensure the new interpreter will not ejected
                # by these tokens (self.tokenstack)
                parent.redirect.eat_token(parent.tokenstack.pop(0))

        more, reuse = parent.redirect.eat_token(token)
        if not more:
            if self.callback:
                self.callback(parent, parent.redirect)

            if reuse:
                parent.tokenstack += parent.redirect.tokenstack[:-1]

            parent.redirect = None
            return self.nextstate, reuse

        return self, False


class Terminate(GoTo):
    def __init__(self, **kw):
        super().__init__(None, **kw)


class Switch(Action):
    def __init__(self, default=None, **kw):
        self.default = default
        self.cases = {k.rstrip('_'): v for k, v in kw.items()}

    def __call__(self, interpreter, token, *args):
        action = self.cases.get(token.string, self.default)
        if action is None:
            raise BadSyntax(interpreter, token, expected=self.cases.keys())

        return action(interpreter, token, *args)


class Interpreter(metaclass=abc.ABCMeta):
    redirect = None

    def __init__(self, initialstate, *args, tokenizer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tokenizer = tokenizer if tokenizer else Tokenizer()
        self.tokenstack = []
        self._set_state(initialstate)

    @property
    @abc.abstractmethod
    def statemap(self):
        raise NotImplementedError()

    def _set_state(self, state):
        if isinstance(state, str):
            self.state = self.statemap[state]
        else:
            self.state = state

    def eat_token(self, token):
        """Eats one token.

        :class:`BadSyntax` and :class:`BadAttribute` will be raised by this
        method.

        :param token: The token to eat.
        :return: tuple(boolean: more, list of tokens)

        """

        if not callable(self.state):
            try:
                self._set_state(self.state[token.type])
            except KeyError:
                validtokens = [
                    EXACT_TOKENS_DICT.get(i, TOKEN_NAMES[i])
                    for i in self.state.keys()
                ]
                raise BadSyntax(self, token, expected=validtokens)

            if not callable(self.state):
                self.tokenstack.append(token)
                return True, None

        newstate, reuse = self.state(self, token)
        if newstate is None:
            # Final token
            return False, reuse

        if newstate != self.state:
            self._set_state(newstate)

        if reuse:
            return self.eat_token(token)

        return True, None
