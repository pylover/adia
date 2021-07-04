from ..renderer import Renderer
from ..sequence import SequenceDiagram

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

    @property
    def box_hpadding(self):
        return 1, int(not(len(self.title) % 2)) + 1

    @property
    def boxlen(self):
        lp, rp = self.box_hpadding
        return len(self.title) + lp + rp + 2

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

    def __init__(self, item, caller, callee, level):
        self.item = item
        self.level = level  # TODO: Maybe remove it
        self.caller = caller
        self.callee = callee

    def __repr__(self):
        return f'{self.repr_symbol} {repr(self.item)}'

    def calc(self):
        self.start = self.caller.middlecol
        self.end = self.callee.middlecol

        if self.start > self.end:
            self.direction = LEFT
            self.start, self.end = self.end, self.start
        else:
            self.direction = RIGHT

        if self.reverse:
            self.direction ^= 1

        self.start += 1
        self.length = self.end - self.start

    def draw(self, canvas, row):
        [canvas.draw_leftarrow, canvas.draw_rightarrow][self.direction](
            self.start, row, self.length, char=self.char
        )


class ItemEndPlan(ItemStartPlan):
    char = '-'
    repr_symbol = '<---'
    reverse = True


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

    def _planitems(self):
        self._itemplans = []

        def _recurse(parent, level=0):
            for item in parent:
                caller = self._moduleplans_dict[item.caller]
                callee = self._moduleplans_dict[item.callee]
                plan = ItemStartPlan(item, caller, callee, level)
                self._itemplans.append(plan)

                if len(item):
                    _recurse(item, level + 1)

                plan = ItemEndPlan(item, caller, callee, level)
                self._itemplans.append(plan)

        _recurse(self.diagram)

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

        self.canvas.extendright(col - self.canvas.cols)
        self._extend(1)

    def _render_emptyline(self):
        for m in self._moduleplans:
            m.drawpipe(self.canvas, self.row)

    def _render_items(self):
        last = None

        for c in self._itemplans:
            self._render_emptyline()
            c.calc()

            if c.direction != last:
                self._extend(1)
                self._render_emptyline()

            last = c.direction
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
