from io import StringIO

from .lazyattr import LazyAttribute
from .container import Container
from .interpreter import Interpreter, GoTo, Switch, Terminate, New
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
            NAME: GoTo('name'),
        },
        'name': {
            NAME: GoTo('name'),
            TILDA: GoTo('name'),
            NEWLINE: Terminate(cb=_finish, limit=False),
            COLON: GoTo(':', limit=False),
        },
        ':': {
            MULTILINE: Terminate(cb=_finish_multiline, limit=False),
            EVERYTHING: {
                NEWLINE: Terminate(cb=_finish, limit=False),
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
                COLON: GoTo(':', limit=False),
                NAME: {
                    COLON: GoTo(':', limit=False),
                },
            },
            COLON: GoTo(':', limit=False),
        }},
        ':': {
            MULTILINE: Terminate(cb=Item._finish_multiline, limit=False),
            EVERYTHING: {
                NEWLINE: Terminate(cb=_finish, limit=False)
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
    returnsign = '=>'

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
        'start': {NAME: {RARROW: {NAME: GoTo('name -> name')}}},
        'name -> name': {
            NEWLINE: Terminate(cb=_complete),
            EOF: Terminate(cb=_complete),
            COLON: GoTo(':'),
        },
        ':': {EVERYTHING: {
            NEWLINE: Terminate(cb=_complete)
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
    title = None
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
                f.write(c.dumps())
                f.write('\n')

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
        'sequence': Terminate(reuse=True),
        'class': Terminate(reuse=True),
        'for': New(Loop, 'start', cb=_new_loop),
        'while': New(Loop, 'start', cb=_new_loop),
        'loop': New(Loop, 'start', cb=_new_loop),
        'if': New(Condition, 'start', cb=_new_condition),
        'alt': New(Condition, 'start', cb=_new_condition),
        'elif': New(Condition, 'start', cb=_new_condition),
        'else': New(Condition, 'start', cb=_new_condition),
    }

    statemap = {
        'title': {
            EVERYTHING: {
                NEWLINE: GoTo('start', cb=_set_title)
            }
        },
        'start': {
            HASH: {EVERYTHING: {NEWLINE: GoTo('start', ignore=True)}},
            NEWLINE: GoTo('start', ignore=True),
            INDENT: GoTo('indent', cb=_indent, ignore=True),
            DEDENT: GoTo('start', cb=_dedent, ignore=True),
            EOF: Terminate(),
            NAME: Switch(default=GoTo('name'), **_keywords),
            AT: GoTo('@', ignore=True),
        },
        'indent': {
            HASH: {EVERYTHING: {NEWLINE: GoTo('start', ignore=True)}},
            NAME: Switch(default=GoTo('  name'), **_keywords),
            AT: GoTo('@', ignore=True),
            NEWLINE: GoTo('start', ignore=True),
            INDENT: GoTo('indent', cb=_indent, ignore=True),
        },
        'name': {
            RARROW: New(Call, 'start', cb=_new_call),
            COLON: GoTo('attr:'),
            DOT: {NAME: {COLON: GoTo('mod.attr:')}},
        },
        '  name': {
            RARROW: New(Call, 'start', cb=_new_call)
        },
        'attr:': {
            EVERYTHING: {NEWLINE: GoTo('start', cb=_attr)}
        },
        'mod.attr:': {
            EVERYTHING: {NEWLINE: GoTo('start', cb=_module_attr)}
        },
        '@': {
            NAME: New(Note, 'start', cb=_new_note),
        }
    }
