from .visible import Visible
from .interpreter import Interpreter, Consume, FinalConsume, New, Ignore, Goto
from .token import *


class Module(Visible):
    def __init__(self, title, type_='module'):
        self.title = title
        self.type = type_


class Call(Visible, Interpreter, list):
    caller = None
    callee = None

    def __init__(self, tokenizer):
        super().__init__(tokenizer, 'call')

    def __repr__(self):
        result = f'{self.caller} -> {self.callee}'
        if self.text:
            result += f': {self.text}'

        if len(self):
            result += '\n'
            for c in self:
                for line in repr(c).splitlines():
                    result += f'  {line}\n'

        return result.rstrip('\n')

    def _complete(self, caller, callee, text=None):
        self.caller = caller
        self.callee = callee
        self.text = text.strip() if text else None

    statemap = {
        'call': {NAME: {RARROW: {NAME: Goto(nextstate='name -> name')}}},
        'name -> name': {
            NEWLINE: FinalConsume(_complete),
            EOF: FinalConsume(_complete),
            COLON: Goto(nextstate=':'),
        },
        ':': {EVERYTHING: {
            NEWLINE: FinalConsume(_complete)
        }}
    }


class SequenceDiagram(Visible, Interpreter, list):
    title = 'Untitled'

    def __init__(self, tokenizer):
        super().__init__(tokenizer, 'start')
        self.modules = {}
        self._callstack = []

    def __repr__(self):
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
                result += repr(c)
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
        self.tokenstack.pop(0)
        if len(self.current):
            self._callstack.append(self.current[-1])

    def _dedent(self):
        if self._callstack:
            self._callstack.pop()

    def _new_call(self, call):
        self._ensuremodule(call.caller)
        self._ensuremodule(call.callee)
        self.current.append(call)

    def _attr(self, attr, value):
        value = value.strip()

        if attr == 'title':
            self.title = value
        else:
            raise AttributeError(attr)

    def _module_attr(self, module, attr, value):
        self._ensuremodule(module)
        if not hasattr(self.modules[module], attr):
            raise AttributeError(module, attr)

        setattr(self.modules[module], attr, value.strip())

    statemap = {
        'start': {
            HASH: {NAME: {NEWLINE: Ignore(nextstate='start')}},
            NEWLINE: Ignore(nextstate='start'),
            INDENT: {
                NAME: Goto(callback=_indent, nextstate='  name'),
            },
            DEDENT: Ignore(callback=_dedent, nextstate='start'),
            EOF: Ignore(nextstate='start'),
            NAME: Goto(nextstate='name'),
        },
        'name': {
            RARROW: New(Call, callback=_new_call, nextstate='start'),
            COLON: Goto(nextstate='attr:'),
            DOT: {NAME: {COLON: Goto(nextstate='mod.attr:')}}
        },
        'attr:': {
            EVERYTHING: {NEWLINE: Consume(_attr, nextstate='start')}
        },
        'mod.attr:': {
            EVERYTHING: {NEWLINE: Consume(_module_attr, nextstate='start')}
        },
        '  name': {
            RARROW: New(Call, callback=_new_call, nextstate='start')
        }
    }
