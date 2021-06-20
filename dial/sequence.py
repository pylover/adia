from .visible import Visible
from .interpreter import Interpreter, Ignore
from .token import *


class Module(Visible):
    def __init__(self, name):
        self.name = name


class Call(Visible):
    def __init__(self, caller, callee):
        self.caller = caller
        self.callee = callee

    def __eq__(self, other):
        if isinstance(other, Call):
            return self.caller == other.caller and \
                self.callee == other.callee


class SequenceDiagram(list, Visible, Interpreter):
    def __init__(self, tokenizer, name):
        super(Visible, self).__init__(tokenizer)
        self.name = name
        self.modules = {}
        self.callstack = []

    def _ensuremodule(self, module):
        if module not in self.modules:
            self.modules[module] = Module(module)

    def _simplecall(self, caller, callee):
        self._ensuremodule(caller)
        self._ensuremodule(callee)
        self.append(Call(caller, callee))
        return 'root'

    def _indent(self, caller):
        self._ensuremodule(caller)
        self.callstack.append(caller)
        return 'caller'

    def _callercallee(self, callee):
        self._ensuremodule(callee)
        self.append(Call(self.callstack[-1], callee))
        return 'caller'

    def _dedent(self):
        self.callstack.pop()
        return 'caller' if self.callstack else 'root'

    states = {
        'root': {
            NEWLINE: Ignore('root'),
            NAME: {
                COLON: {
                    NAME: {
                        NEWLINE: _simplecall,
                    },
                    NEWLINE: {
                        INDENT: _indent
                    }
                }
            },
            EOF: Ignore('root')
        },
        'caller': {
            NAME: {
                NEWLINE: _callercallee,
            },
            DEDENT: _dedent,
        }
    }
