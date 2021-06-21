from .visible import Visible
from .interpreter import Interpreter, Ignore, Goto, Hook
from .token import *


class Module(Visible):
    def __init__(self, name):
        self.name = name


class Function:
    def __init__(self, module, name=None, args=None, returns=None):
        self.module = module
        self.name = name
        self.args = args or []
        self.returns = returns

    def __repr__(self):
        result = f'{self.module}'
        if self.name:
            args = ', '.join(self.args) if self.args else ''
            result += f'.{self.name}({args})'

        return result


class Call(list, Visible):
    def __init__(self, caller, callee, children=None):
        self.caller = caller
        self.callee = callee
        if children:
            super(Call, self).__init__(children)

        super(list, self).__init__()

    def __repr__(self):
        result = f'{self.caller} -> {self.callee}'

        if self:
            result += ':\n'
            for c in self:
                r = repr(c)
                for l in r.splitlines():
                    result += '  ' + l + '\n'

        if result.endswith('\n'):
            result = result[:-1]

        return result


class SequenceDiagram(list, Visible, Interpreter):
    def __init__(self, tokenizer, name):
        super(Visible, self).__init__(tokenizer, 'start')
        self.name = name
        self.modules = {}

        # Parser states
        self._caller = None
        self._callstack = []
        self._level = 0

    def _ensuremodule(self, name):
        if name not in self.modules:
            self.modules[name] = Module(name)

    @property
    def _parent(self):
        if self._callstack:
            return self._callstack[-1]

        return self

    def _create_call(self, module, name=None, *args):
        self._ensuremodule(module)
        callee = Function(module, name, args)
        call = Call(self._caller, callee)
        self._parent.append(call)
        return call

    # Parser functions
    def _eat_caller(self, module, name=None, *args):
        self._ensuremodule(module)
        if self._level:
            call = self._create_call(module, name, *args)
            self._callstack.append(call)
            self._caller = call.callee
        else:
            self._caller = Function(module, name, args)

    def _eat_callee(self, module, name=None, *args):
        self._ensuremodule(module)
        callee = Function(module, name, args)
        self._parent.append(Call(self._caller, callee))

    def _eat_indent(self):
        self._level += 1

    def _eat_dedent(self):
        self._level -= 1
        if self._callstack:
            call = self._callstack.pop()
            self._caller = call.caller
        else:
            self._caller = None

    def _self_call(self, funcname):
        if self._caller is None:
            self._eat_caller(funcname)
            self.tokenstack.append(self._caller.module)
        else:
            self.tokenstack.append(self._caller.module)
            self.tokenstack.append(funcname)

    states = {
        'start': {
            NEWLINE: Ignore(),
            EOF: Ignore(),
            NAME: {
                COLON: Hook(_eat_caller, ':'),
                DOT: Goto('.'),
                NEWLINE: Hook(_eat_callee, 'start'),
                LPAR: Hook(_self_call, '('),
            },
            DEDENT: Hook(_eat_dedent, 'start'),
        },
        ':': {
            NAME: {
                NEWLINE: Hook(_eat_callee, 'start'),
                DOT: Goto('.'),
            },
            NEWLINE: {
                INDENT: Hook(_eat_indent, 'start'),
            }
        },
        '.': {
            NAME: {
                LPAR: Goto('('),
            }
        },
        '(': {
            RPAR: Goto(')'),
            NAME: {
                COMMA: Goto('('),
                RPAR: Goto(')'),
            }
        },
        ')': {
            NEWLINE: Hook(_eat_callee, 'start'),
            COLON: Hook(_eat_caller, ':'),
        },
    }
