from ..renderer import Renderer
from ..sequence import SequenceDiagram, Call, Condition

from .canvas import ASCIICanvas


LEFT = 0
RIGHT = 1


def twiniter(l):
    if not hasattr(l, '__next__'):
        l = iter(l)

    try:
        f = next(l)
        while True:
            n = next(l)
            yield f, n
            f = n
    except StopIteration:
        yield f, None


class ASCIIRenderer(Renderer):
    def __init__(self, diagram, canvas=None):
        self.diagram = diagram
        if canvas is None:
            self.canvas = ASCIICanvas()
        else:
            self.canvas = canvas

    def _extend(self, i):
        self.canvas.extendbottom(i)

    @property
    def row(self):
        return self.canvas.rows - 1


class ASCIIDiagramRenderer(ASCIIRenderer):
    def render(self):
        self._render_header()

        for unit in self.diagram:
            if isinstance(unit, SequenceDiagram):
                ASCIISequenceRenderer(unit, self.canvas).render()

        return self.canvas

    def _render_header(self):
        dia = self.diagram
        self._extend(1)
        self.canvas.write_textline(1, self.row, f'DIAGRAM: {dia.title} ')

        if dia.author:
            self._extend(1)
            self.canvas.write_textline(1, self.row, f'author: {dia.author} ')

        if dia.version:
            self._extend(1)
            self.canvas.write_textline(1, self.row, f'version: {dia.version} ')

        self._extend(1)


class Plan:
    pass


class ModulePlan(Plan):
    col = 0
    row = 0
    lpad = 1
    rpad = 1

    def __init__(self, module):
        self.module = module

    def __repr__(self):
        return f'ModulePlan: {self.title}'

    # TODO: lazyattr
    @property
    def box_hpadding(self):
        return 1, int(not(len(self.title) % 2)) + 1

    # TODO: lazyattr
    @property
    def boxlen(self):
        lp, rp = self.box_hpadding
        return len(self.title) + lp + rp + 2

    # TODO: lazyattr
    @property
    def title(self):
        return self.module.title

    @property
    def middlecol(self):
        return self.col + self.boxlen // 2

    def drawbox(self, canvas, col=None, row=None):
        if col:
            self.col = col

        if row:
            self.row = row

        canvas.draw_textbox(self.col, self.row, self.title,
                            hpadding=(self.box_hpadding))

    def drawpipe(self, canvas, row):
        canvas.set_char(self.middlecol, row, '|')


class ItemStartPlan(Plan):
    char = '~'
    repr_symbol = '~~~>'
    reverse = False
    direction = RIGHT
    length = 0
    start = 0
    end = 0

    def __init__(self, item, caller, callee, direction, level):
        self.item = item
        self.level = level  # TODO: Maybe remove it
        self.caller = caller
        self.callee = callee
        self.direction = direction

    def __repr__(self):
        return f'{self.repr_symbol} {repr(self.item)}'

    # TODO: lazyattr
    @property
    def text(self):
        return self.item.text

    # TODO: lazyattr
    @property
    def textlen(self):
        if self.text:
            return len(self.text)

        return 0

    def calc(self):
        self.start = self.caller.middlecol
        self.end = self.callee.middlecol

        if self.start > self.end:
            self.start, self.end = self.end, self.start

        self.start += 1
        self.length = self.end - self.start

    def draw(self, canvas, row):
        [canvas.draw_leftarrow, canvas.draw_rightarrow][self.direction](
            self.start, row, self.length, char=self.char, text=self.text
        )


class ItemEndPlan(ItemStartPlan):
    char = '-'
    repr_symbol = '<---'
    reverse = True

    @property
    def text(self):
        return None


class ConditionPlan(Plan):
    def __init__(self, item, level):
        self.item = item
        self.level = level


class ASCIISequenceRenderer(ASCIIRenderer):
    _moduleplans = None
    _moduleplans_dict = None
    _itemplans = None

    def _planmodules(self):
        self._moduleplans = []
        self._moduleplans_dict = {}

        for m in self.diagram.modules_order:
            module = ModulePlan(self.diagram.modules[m])
            self._moduleplans.append(module)
            self._moduleplans_dict[m] = module

    def _fromto_modules(self, from_, to, reverse=False):
        capt = False

        it = self._moduleplans
        if reverse:
            it = reversed(it)

        for m, nm in twiniter(it):
            if not capt and m is not from_:
                continue

            if m is from_:
                capt = True

            if capt:
                if m is to:
                    yield m, None
                    return
                yield m, nm

    def _availspace(self, from_, to, reverse=False):
        result = 0
        for m, nm in self._fromto_modules(from_, to, reverse):
            result += m.boxlen
            if nm is None:
                continue

            if reverse:
                result += max(m.lpad, nm.rpad)
            else:
                result += max(m.rpad, nm.lpad)

        result -= from_.boxlen // 2 + 1
        result -= to.boxlen // 2 + 1
        return result - 5

    def _plancondition(self, item, level):
        condstart_plan = ConditionPlan(item, level)

        self._itemplans.append(condstart_plan)

        if len(item):
            self._recurse(item, level + 1)

        condend_plan = ConditionPlan(item, level)
        self._itemplans.append(condend_plan)

    def _plancall(self, item, level):
        caller = self._moduleplans_dict[item.caller]
        callee = self._moduleplans_dict[item.callee]
        diff = self._moduleplans.index(callee) - \
            self._moduleplans.index(caller)

        dir_ = LEFT if diff < 0 else RIGHT
        itemplan = ItemStartPlan(item, caller, callee, dir_, level)

        self._itemplans.append(itemplan)

        avail = self._availspace(caller, callee, reverse=dir_ == LEFT)
        if itemplan.textlen > avail:
            if dir_ == LEFT:
                callee.rpad += itemplan.textlen - avail
            else:
                callee.lpad += itemplan.textlen - avail

        if len(item):
            self._recurse(item, level + 1)

        itemplan = ItemEndPlan(item, caller, callee, not(dir_), level)
        self._itemplans.append(itemplan)

    def _recurse(self, parent, level):
        for item in parent:
            if isinstance(item, Call):
                self._plancall(item, level)
            elif isinstance(item, Condition):
                self._plancondition(item, level)

    def _planitems(self):
        self._itemplans = []
        self._recurse(self.diagram, 0)

    def plan(self):
        self._planmodules()
        self._planitems()

    # Sequence
    def _render_modules(self):
        if not self._moduleplans:
            return

        self._extend(1)
        fm = self._moduleplans[0]
        row = self.row
        col = max(1, fm.lpad)

        for m, nm in twiniter(self._moduleplans):
            m.drawbox(self.canvas, col, row)
            col += m.boxlen + max(m.rpad, nm.lpad if nm else 1)

        if col > self.canvas.cols:
            self.canvas.extendright(col - self.canvas.cols)

        self._extend(1)

    def _render_emptyline(self):
        for m in self._moduleplans:
            m.drawpipe(self.canvas, self.row)

    def _render_items(self):
        lastdir = None
        lasttype = None

        for c in self._itemplans:
            self._render_emptyline()
            c.calc()

            if c.direction != lastdir or not lasttype or \
                    not isinstance(c, lasttype):
                self._extend(1)
                self._render_emptyline()

            lastdir = c.direction
            lasttype = type(c)
            c.draw(self.canvas, self.row)
            self._extend(1)

    def render(self):
        self.plan()

        # Sequence Header
        if self.diagram.title:
            self._extend(1)
            self.canvas.write_textline(
                1, self.row, f'SEQUENCE: {self.diagram.title} ')
            self._extend(1)

        self._render_modules()
        self._render_emptyline()
        self._render_items()
        self._render_emptyline()
        self._render_modules()
