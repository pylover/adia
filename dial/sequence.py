from .visible import Visible
from .interpreter import Interpreter, Ignore
from .token import *


class Module(Visible):
    def __init__(self, name):
        self.name = name


class Call(list, Visible):
    def __init__(self, caller, callee, children=None):
        self.caller = caller
        self.callee = callee
        if children:
            super(Call, self).__init__(children)

        super(list, self).__init__()

    def __ne__(self, other):
        if isinstance(other, Call):
            if len(self) != len(other):
                return True

            for i, c in enumerate(self):
                if c != other[i]:
                    return True

            return self.caller != other.caller or \
                self.callee != other.callee

        return super().__ne__(other)

    def __eq__(self, other):
        if isinstance(other, Call):
            return not self.__ne__(other)

        return super().__eq__(other)

    def __repr__(self):
        result = f'{self.caller} -> {self.callee}'
        if self:
            result += ':\n'
            for c in self:
                r = repr(c)
                for l in r.splitlines():
                    result += '  ' + l + '\n'

        return result


class SequenceDiagram(list, Visible, Interpreter):
    def __init__(self, tokenizer, name):
        super(Visible, self).__init__(tokenizer)
        self.name = name
        self.modules = {}
        self.callerstack = []
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
        self.callerstack.append(caller)
        return 'caller'

    def _dedent(self):
        self.callerstack.pop()
        if self.callstack:
            self.callstack.pop()
        return 'caller' if self.callerstack else 'root'

    def _newcall(self, callee):
        self._ensuremodule(callee)
        call = Call(self.callerstack[-1], callee)

        if self.callstack:
            self.callstack[-1].append(call)
        else:
            self.append(call)

        return call

    def _callercallee(self, callee):
        self._newcall(callee)
        return 'caller'

    def _callercalleecaller(self, callee):
        call = self._newcall(callee)
        self.callstack.append(call)
        return self._indent(callee)

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
                COLON: {
                    NEWLINE: {
                        INDENT: _callercalleecaller,
                    }
                }
            },
            DEDENT: _dedent,
        }
    }
