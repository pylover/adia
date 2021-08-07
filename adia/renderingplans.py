import abc

from .lazyattr import LazyAttribute
from .constants import RIGHT, LEFT


class RenderingPlan:
    # TODO: Remove or add some common members or abstract interface.
    pass


class ModulePlan(RenderingPlan):
    col = 0
    row = 0

    def __init__(self, module, lpad=0, rpad=0):
        self.module = module
        self.lpad = lpad
        self.rpad = rpad

    def __repr__(self):
        return f'ModulePlan: {self.title}'

    @LazyAttribute
    def box_hpadding(self):
        return 1, int(not(len(self.title) % 2)) + 1

    @LazyAttribute
    def boxlen(self):
        lp, rp = self.box_hpadding
        return len(self.title) + lp + rp + 2

    @LazyAttribute
    def title(self):
        return self.module.title

    @property
    def middlecol(self):
        return self.col + self.boxlen // 2

    def drawbox(self, renderer, col=None, row=None):
        if col:
            self.col = col

        if row:
            self.row = row

        renderer.canvas.draw_textbox(
            self.col, self.row, self.title, hpadding=(self.box_hpadding))

    def drawpipe(self, renderer, row):
        renderer.canvas.set_char(self.middlecol, row, '|')


class ItemPlan(RenderingPlan, metaclass=abc.ABCMeta):
    char = '!'
    repr_symbol = '!!!!'
    direction = RIGHT
    length = 0
    start = 0
    end = 0

    def __init__(self, item, direction, level):
        self.item = item
        self.level = level
        self.direction = direction

    def __repr__(self):
        return f'{self.repr_symbol} {repr(self.item)}'

    @LazyAttribute
    def textwidth(self):
        if self.text:
            return len(self.text)

        return 0

    @property
    def kind(self):
        return self.item.kind

    @property
    def text(self):
        return self.item.text

    @abc.abstractmethod
    def calc(self):
        raise NotImplementedError()


class ItemStartPlan(ItemPlan):
    char = '~'
    repr_symbol = '~~~>'
    reverse = False
    selfcall = False

    def __init__(self, item, caller, callee, direction, level):
        super().__init__(item, direction, level)
        self.caller = caller
        self.callee = callee
        if caller is callee:
            self.selfcall = True

    def _calc_selfcall(self):
        self.start = self.caller.middlecol

        linelen = 0
        if self.item.text:
            linelen = len(self.item.text)

        if self.item.returntext:
            linelen = max(len(self.item.returntext), linelen)

        self.length = linelen + 6
        self.start += 1
        self.end = self.start + self.length
        return 0, 1, 0

    def _calc_otherscall(self):
        self.start = self.caller.middlecol
        self.end = self.callee.middlecol

        if self.start > self.end:
            self.start, self.end = self.end, self.start

        self.start += 1
        self.length = self.end - self.start

        return 0, 1, 0

    def calc(self):
        if self.selfcall:
            return self._calc_selfcall()
        else:
            return self._calc_otherscall()

    def draw(self, renderer, row):
        canvas = renderer.canvas

        canvas.draw_hline(self.start, row, self.length, char=self.char)
        if self.direction == LEFT:
            canvas.set_char(self.start, row, '<')
        else:
            canvas.set_char(self.end - 1, row, '>')

        if self.text:
            canvas.write_textline(self.start + 3, row, self.text)

        if not self.selfcall:
            return

        canvas.set_char(self.end, row, '+')
        canvas.set_char(self.end - 1, row, self.char)
        renderer.register_repeat(self.end, '|')


class ItemEndPlan(ItemStartPlan):
    char = '-'
    repr_symbol = '<---'
    reverse = True

    @property
    def text(self):
        return self.item.returntext

    def draw(self, renderer, row):
        super().draw(renderer, row)

        if not self.selfcall:
            return

        renderer.unregister_repeat(self.end, '|')


class ConditionStartPlan(ItemPlan):
    char = '*'
    startmodule = None
    endmodule = None
    children = None

    def __init__(self, item, startmodule, endmodule, level):
        super().__init__(item, RIGHT, level)
        self.startmodule = startmodule
        self.endmodule = endmodule

    @property
    def singlemodule(self):
        return self.startmodule is self.endmodule

    @LazyAttribute
    def text(self):
        result = f'{self.item.kind}'
        if self.item.text:
            result += f' {self.item.text}'

        return result

    def _calc_singlemodule(self):
        self.start = self.startmodule.col

        linelen = 0
        if self.item.text:
            linelen = len(self.item.text)

        self.length = linelen + 7
        self.end = self.start + self.length
        self.end -= 1
        return 0, 3, 0

    def _calc_multimodule(self):
        self.start = self.startmodule.col
        self.end = self.endmodule.col + self.endmodule.boxlen
        self.length = self.end - self.start
        self.end -= 1
        return 0, 3, 0

    def calc(self):
        if self.startmodule is None:
            self.start = 0
            self.length = max(10, self.textwidth + 4)
            self.end = self.length - 1
            return 0, 3, 0

        if self.singlemodule:
            return self._calc_singlemodule()
        else:
            return self._calc_multimodule()

    def draw(self, renderer, row):
        canvas = renderer.canvas

        canvas.draw_hline(self.start, row, self.length, char=self.char)

        row += 1
        canvas.write_textline(self.start, row, ' ' * self.length)
        canvas.set_char(self.start, row, '*')
        canvas.set_char(self.end, row, '*')
        canvas.write_textline(self.start + 2, row, self.text)

        row += 1
        canvas.draw_hline(self.start, row, self.length, char=self.char)


class ConditionEndPlan(ConditionStartPlan):

    @property
    def text(self):
        if self.kind in ('if', 'elif', 'else'):
            return 'end if'

        return f'end {self.kind}'


class NotePlan(ItemPlan):
    char = '-'
    repr_symbol = '@'
    startmodule = None
    endmodule = None

    def __init__(self, item, startmodule, endmodule, level):
        super().__init__(item, RIGHT, level)
        self.startmodule = startmodule
        self.endmodule = endmodule

    @LazyAttribute
    def lines(self):
        return self.text.splitlines()

    @LazyAttribute
    def textwidth(self):
        return max(len(x) for x in self.lines)

    def calc(self):
        self.start = self.startmodule.col

        if self.endmodule is None:
            self.length = self.startmodule.boxlen
        else:
            self.length = (self.endmodule.col + self.endmodule.boxlen) - \
                self.start

        self.length = max(self.length, self.textwidth + 4)
        self.end = self.start + self.length
        return 0, len(self.lines) + 2, 0

    def draw(self, renderer, row):
        canvas = renderer.canvas

        canvas.draw_hline(self.start, row, self.length, char=self.char)

        for linelen in self.lines:
            row += 1
            canvas.write_textline(self.start, row, ' ' * self.length)
            canvas.write_textline(self.start + 2, row, linelen)
            canvas.set_char(self.start, row, '|')
            canvas.set_char(self.end - 1, row, '|')

        row += 1
        canvas.draw_hline(self.start, row, self.length, char=self.char)
