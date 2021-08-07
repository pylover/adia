from io import StringIO

from .lazyattr import LazyAttribute
from .container import Container
from .interpreter import Interpreter, Consume, Final, FinalConsume, New, \
    Ignore, Goto, Switch
from .token import NAME, NEWLINE, EVERYTHING, RARROW, COLON, AT, HASH, EOF, \
    DOT, DEDENT, INDENT, MULTILINE, TILDA


class Module:
    title = None
    type = 'module'

    def __init__(self, title):
        self.title = title


class Item(Interpreter):
    kind = None
    args = None
    text = None
    multiline = None

    def __init__(self, *args, **kw):
        super().__init__('start', *args, **kw)

    def _complete(self, kind, *args, text=None, multiline=False):
        self.kind = kind
        self.args = args
        self.text = text.strip() if text else None
        self.multiline = multiline

    def _finish_multiline(self, kind, *args):
        return self._finish(kind, *args, multiline=True)

    def _finish(self, kind, *args, **kw):
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
        return self._complete(kind, *nargs, text=text, **kw)

    @property
    def left(self):
        return self.kind

    @property
    def right(self):
        return self.text

    def __repr__(self):
        return f'SequenceItem: {self.left}'

    def dumps(self):
        f = StringIO()
        f.write(self.left)

        if self.right:
            f.write(': ')
            if self.multiline:
                f.write('|\n')
                for line in self.right.splitlines():
                    f.write(f'  {line}\n')
            else:
                f.write(f'{self.right}')

        return f.getvalue()

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

    @LazyAttribute
    def modules(self):
        result = []
        for m in self.args:
            if m == '~':
                continue
            result.append(m)

        return result

    @LazyAttribute
    def left(self):
        result = self.kind

        if self.args:
            result += f'{" ".join(self.args)}'

        return result

    def _finish(self, *args, **kw):
        super()._finish('@', *args, **kw)

    statemap = {
        'start': {NAME: {
            TILDA: {
                COLON: Goto(nextstate=':'),
                NAME: {
                    COLON: Goto(nextstate=':'),
                },
            },
            COLON: Goto(nextstate=':'),
        }},
        ':': {
            MULTILINE: FinalConsume(Item._finish_multiline, alltokens=True),
            EVERYTHING: {
                NEWLINE: FinalConsume(_finish, alltokens=True)
            }
        },
    }


class ContainerItem(Item, Container):

    def dumps(self):
        f = StringIO()
        f.write(super().dumps())

        if len(self):
            f.write('\n')
            for c in self:
                for line in c.dumps().splitlines():
                    f.write(f'  {line}\n')

        return f.getvalue().rstrip('\n')


class Call(ContainerItem):
    caller = None
    callee = None
    returntext = None
    returnsign = '->'

    @LazyAttribute
    def left(self):
        return f'{self.caller} -> {self.callee}'

    @LazyAttribute
    def right(self):
        if not self.text:
            return

        f = StringIO()
        f.write(self.text)
        if self.returntext:
            f.write(f' {self.returnsign} {self.returntext}')

        return f.getvalue()

    def _complete(self, caller, callee, text=None):
        self.caller = caller
        self.callee = callee
        if text and self.returnsign in text:
            text, returntext = text.rsplit(self.returnsign, 1)
            self.returntext = returntext.strip()
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


class Loop(ContainerItem):
    pass


class Condition(ContainerItem):
    pass


class SequenceDiagram(Interpreter, Container):
    """Represents a sequence diagram.

    The :class:`adia.diagram` class creates an instance of this class for
    each sequence diagram section.

    """
    title = 'Untitled Sequence Diagram'
    description = None
    tags = None

    def __init__(self, *args, **kwargs):
        super().__init__('title', *args, **kwargs)
        self.modules = {}
        self.modules_order = []
        self._callstack = []

    def __repr__(self):
        return f'SequenceDiagram: {self.title}'

    def dumps(self):
        f = StringIO()
        f.write('sequence:')

        if self.title:
            f.write(f' {self.title}')

        f.write('\n')

        if self.description:
            f.write(f'description: {self.description}\n')

        if self.tags:
            f.write(f'tags: {self.tags}\n')

        modattrs = []
        for k, v in sorted(self.modules.items()):
            if k != v.title:
                modattrs.append((k, 'title', v.title))

            if 'module' != v.type:
                modattrs.append((k, 'type', v.type))

        if modattrs:
            f.write('\n# Modules\n')
            for m, a, v in modattrs:
                f.write(f'{m}.{a}: {v}\n')

        if len(self):
            f.write('\n')
            for c in self:
                f.write(f'{c.dumps()}\n')

        return f.getvalue()

    def _ensuremodule(self, name, visible=False):
        if name not in self.modules:
            self.modules[name] = Module(name)

        if visible and name not in self.modules_order:
            self.modules_order.append(name)

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
        self._ensuremodule(call.caller, visible=True)
        self._ensuremodule(call.callee, visible=True)
        self.current.append(call)

    def _new_note(self, note):
        for m in note.modules:
            self._ensuremodule(m, visible=False)

        self.current.append(note)

    def _new_loop(self, loop):
        self.current.append(loop)

    def _new_condition(self, condition):
        self.current.append(condition)

    def _attr(self, attr, value):
        value = value.strip()

        if attr == 'description':
            self.description = value
        elif attr == 'tags':
            self.tags = value
        else:
            raise AttributeError(attr)

    def _set_title(self, value):
        self.title = value.strip()

    def _module_attr(self, module, attr, value):
        if not hasattr(Module, attr):
            raise AttributeError(module, attr)

        self._ensuremodule(module)
        setattr(self.modules[module], attr, value.strip())

    _keywords = {
        'sequence': Final(nextstate='sequence'),
        'state': Final(nextstate='start'),
        'class': Final(nextstate='start'),
        'for': New(Loop, callback=_new_loop, nextstate='start'),
        'while': New(Loop, callback=_new_loop, nextstate='start'),
        'loop': New(Loop, callback=_new_loop, nextstate='start'),
        'if': New(Condition, callback=_new_condition, nextstate='start'),
        'alt': New(Condition, callback=_new_condition, nextstate='start'),
        'elif': New(Condition, callback=_new_condition, nextstate='start'),
        'else': New(Condition, callback=_new_condition, nextstate='start'),
    }

    statemap = {
        'title': {
            EVERYTHING: {
                NEWLINE: Consume(_set_title, nextstate='start')
            }
        },
        'start': {
            HASH: {EVERYTHING: {NEWLINE: Ignore(nextstate='start')}},
            NEWLINE: Ignore(nextstate='start'),
            INDENT: Ignore(callback=_indent, nextstate='indent'),
            DEDENT: Ignore(callback=_dedent, nextstate='start'),
            EOF: Final(nextstate='start'),
            NAME: Switch(default=Goto(nextstate='name'), **_keywords),
            AT: Ignore(nextstate='@'),
        },
        'indent': {
            HASH: {EVERYTHING: {NEWLINE: Ignore(nextstate='start')}},
            NAME: Switch(default=Goto(nextstate='  name'), **_keywords),
            AT: Ignore(nextstate='@'),
            NEWLINE: Ignore(nextstate='start'),
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
