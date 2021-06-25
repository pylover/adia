from .visible import Visible
from .interpreter import Interpreter, Consume, FinalConsume, New, Ignore, \
    Goto, Switch
from .token import *


class Module(Visible):
    title = None
    type = 'module'

    def __init__(self, title):
        self.title = title


class Item(Visible, Interpreter):
    type_ = None
    args = None
    text = None
    multiline = None

    def __init__(self, *args, **kw):
        super().__init__('start', *args, **kw)

    def _complete(self, type_, *args, text=None, multiline=False):
        self.type_ = type_
        self.args = args
        self.text = text.strip() if text else None
        self.multiline = multiline

    def _finish_multiline(self, type_, *args):
        return self._finish(type_, *args, multiline=True)

    def _finish(self, type_, *args, **kw):
        args = list(args)
        nargs = []
        while args:
            a = args.pop(0)
            if a == ':':
                break

            nargs.append(a)

        if args:
            text = args[0]
        else:
            text = None
        return self._complete(type_, *nargs, text=text, **kw)

    @property
    def _short_repr(self):
        return self.type_
    
    def dumps(self):
        result = self._short_repr

        if self.text:
            result += ': '

            if self.multiline:
                result += '|\n'
                for l in self.text.splitlines():
                    result += f'  {l}\n'
            else:
                result += f'{self.text}'

        return result

    statemap = {
        'start': {
            NAME: Goto(nextstate='name'),
        },
        'name': {
            NAME: Goto(nextstate='name'),
            TILDA: Goto(nextstate='name'),
            NEWLINE: FinalConsume(_finish, alltokens=True),
            COLON: Goto(nextstate=':'),
        },
        ':': {
            MULTILINE: FinalConsume(_finish_multiline, alltokens=True),
            EVERYTHING: {
                NEWLINE: FinalConsume(_finish, alltokens=True)
            }
        },
    }


class Note(Item):
    multiline = False

    @property
    def position(self):
        return self.type_

    @property
    def modules(self):
        for m in self.args:
            if m == '~':
                continue
            yield m

    def _complete(self, type_, *args, **kw):
        args = list(args)

        if args and args[0] == 'of':
            args.pop(0)

        super()._complete(type_, *args, **kw)

    @property
    def _short_repr(self):
        result = f'@{self.position}'

        if self.position != 'over':
            result += ' of'

        if self.args:
            result += f' {" ".join(self.args)}'

        return result


class Container(Item, list):

    def dumps(self):
        result = super().dumps()

        if len(self):
            result += '\n'
            for c in self:
                for line in c.dumps().splitlines():
                    result += f'  {line}\n'

        return result.rstrip('\n')


class Call(Container):
    caller = None
    callee = None

    @property
    def _short_repr(self):
        return f'{self.caller} -> {self.callee}'

    def _complete(self, caller, callee, text=None):
        self.caller = caller
        self.callee = callee
        super()._complete('call', text=text)

    statemap = {
        'start': {NAME: {RARROW: {NAME: Goto(nextstate='name -> name')}}},
        'name -> name': {
            NEWLINE: FinalConsume(_complete),
            EOF: FinalConsume(_complete),
            COLON: Goto(nextstate=':'),
        },
        ':': {EVERYTHING: {
            NEWLINE: FinalConsume(_complete)
        }}
    }


class Loop(Container):
    pass


class Condition(Container):
    pass


class SequenceDiagram(Visible, Interpreter, list):
    title = 'Untitled'

    def __init__(self, *args, **kwargs):
        super().__init__('start', *args, **kwargs)
        self.modules = {}
        self._callstack = []

    def dumps(self):
        result = f'# Sequence\ntitle: {self.title}\n'

        attrs = ''
        for k, v in self.modules.items():
            if k != v.title:
                attrs += f'{k}.title: {v.title}\n'

            if 'module' != v.type:
                attrs += f'{k}.type: {v.type}\n'

        if attrs:
            result += f'\n{attrs}'

        if len(self):
            result += '\n'
            for c in self:
                result += c.dumps()
                result += '\n'

        return result.rstrip('\n')

    def _ensuremodule(self, name):
        if name not in self.modules:
            self.modules[name] = Module(name)

    @property
    def current(self):
        if self._callstack:
            return self._callstack[-1]

        return self

    def _indent(self):
        if len(self.current):
            self._callstack.append(self.current[-1])

    def _dedent(self):
        if self._callstack:
            self._callstack.pop()

    def _new_call(self, call):
        self._ensuremodule(call.caller)
        self._ensuremodule(call.callee)
        self.current.append(call)

    def _new_note(self, note):
        for m in note.modules:
            self._ensuremodule(m)
        self.current.append(note)

    def _new_loop(self, loop):
        self.current.append(loop)

    def _new_condition(self, condition):
        self.current.append(condition)

    def _attr(self, attr, value):
        value = value.strip()

        if attr == 'title':
            self.title = value
        else:
            raise AttributeError(attr)

    def _module_attr(self, module, attr, value):
        if not hasattr(Module, attr):
            raise AttributeError(module, attr)

        self._ensuremodule(module)
        setattr(self.modules[module], attr, value.strip())

    _keywords = {
        'for': New(Loop, callback=_new_loop, nextstate='start'),
        'while': New(Loop, callback=_new_loop, nextstate='start'),
        'loop': New(Loop, callback=_new_loop, nextstate='start'),
        'if': New(Condition, callback=_new_condition, nextstate='start'),
        'alt': New(Condition, callback=_new_condition, nextstate='start'),
        'elif': New(Condition, callback=_new_condition, nextstate='start'),
        'else': New(Condition, callback=_new_condition, nextstate='start'),
    }

    statemap = {
        'start': {
            HASH: {EVERYTHING: {NEWLINE: Ignore(nextstate='start')}},
            NEWLINE: Ignore(nextstate='start'),
            INDENT: Ignore(callback=_indent, nextstate='indent'),
            DEDENT: Ignore(callback=_dedent, nextstate='start'),
            EOF: Ignore(nextstate='start'),
            NAME: Switch(default=Goto(nextstate='name'), **_keywords),
            AT: Ignore(nextstate='@'),
        },
        'indent': {
            HASH: {EVERYTHING: {NEWLINE: Ignore(nextstate='start')}},
            NAME: Switch(default=Goto(nextstate='  name'), **_keywords),
            AT: Ignore(nextstate='@'),
        },
        'name': {
            RARROW: New(Call, callback=_new_call, nextstate='start'),
            COLON: Goto(nextstate='attr:'),
            DOT: {NAME: {COLON: Goto(nextstate='mod.attr:')}},
        },
        '  name': {
            RARROW: New(Call, callback=_new_call, nextstate='start')
        },
        'attr:': {
            EVERYTHING: {NEWLINE: Consume(_attr, nextstate='start')}
        },
        'mod.attr:': {
            EVERYTHING: {NEWLINE: Consume(_module_attr, nextstate='start')}
        },
        '@': {
            NAME: New(Note, callback=_new_note, nextstate='start'),
        }
    }

    def feedline(self, line):
        if len(line) and not line.endswith('\n'):
            line += '\n'

        for token in self.tokenizer.tokenizeline(line):
            self.eat_token(token)

    def feed(self, string):
        for token in self.tokenizer.tokenizes(string):
            self.eat_token(token)
    
    @classmethod
    def loads(cls, string):
        diagram = cls()
        diagram.feed(string)
        return diagram
