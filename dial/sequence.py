from .visible import Visible
from .interpreter import Interpreter, Ignore, Callback
from .token import *


class Module(Visible):
    def __init__(self, name):
        self.name = name


class Call(Visible):
    def __init__(self, caller, callee):
        self.caller = caller
        self.callee = callee


class SequenceDiagram(list, Visible, Interpreter):
    def __init__(self, tokenizer, name):
        super(Visible, self).__init__(tokenizer)
        self.name = name
        self.modules = {}

    def _ensuremodule(self, module):
        if module not in self.modules:
            self.modules[module] = Module(module)

    def _simplecall(self, caller, callee):
        self._ensuremodule(caller)
        self._ensuremodule(callee)
        self.append(Call(caller, callee))

    states = {
        'root': {
            NEWLINE: Ignore('root'),
            NAME: {
                COLON: {
                    NAME: {
                        NEWLINE: Callback(_simplecall, 'root'),
                    },
                    NEWLINE: {
                        INDENT: Ignore('root')
                    }
                }
            }
        },
    }
