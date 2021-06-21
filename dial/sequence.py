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


class Note(Visible):
    def __init__(self, content, position, module):
        self.content = content
        self.position = position
        self.module = module
        super().__init__()

    def __repr__(self):
        result = f'@note {self.position}'
        if self.module:
            result += f' of {self.module}'

        if self.content:
            result += f': {self.content}'

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
        self._keywords = None

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

    def _eat_keyword(self, *keywords):
        self._keywords = keywords

    def _eat_keyword_value(self, *values):
        if self._keywords[0] == 'note':
            position = self._keywords[1] if len(self._keywords) > 1 else 'left'
            module = self._caller.module if self._caller else \
                self._parent[-1] if self._parent else None
            self._parent.append(Note(
                ' '.join(values),
                position,
                module
            ))

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
            AT: Goto('@'),
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
        '@': {
            NAME: Goto('@...'),
        },
        '@...': {
            COLON: Hook(_eat_keyword, '@...:'),
            NAME: Goto('@...'),
        },
        '@...:': {
            NAME: Goto('@...:'),
            NEWLINE: Hook(_eat_keyword_value, 'start')
        },
    }
