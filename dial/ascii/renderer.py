from ..renderer import Renderer
from ..sequence import SequenceDiagram

from .canvas import ASCIICanvas


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
        if len(self.title) % 2 == 0:
            self.rpad = 2

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

    def drawbox(self, canvas, col=None, row=None):
        if col:
            self.col = col

        if row:
            self.row = row

        canvas.draw_textbox(self.col, self.row, self.title,
                            hpadding=(self.box_hpadding))

    def drawpipe(self, canvas, row):
        canvas.set_char(self.col + self.boxlen // 2, row, '|')


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


class ASCIISequenceRenderer(ASCIIRenderer):
    modules = None

    def _planmodules(self):
        self.modules = []

        for m in self.diagram.modules_order:
            module = ModulePlan(self.diagram.modules[m])
            self.modules.append(module)

    def plan(self):
        self._planmodules()
        # self._plancallstack()

    # Sequence
    def _render_modules(self):
        if not self.modules:
            return

        self._extend(1)
        fm = self.modules[0]
        row = self.row
        col = max(1, fm.lpad)

        for m, nm in twiniter(self.modules):
            m.drawbox(self.canvas, col, row)
            col += m.boxlen + max(m.rpad, nm.lpad if nm else 1)

        self.canvas.extendright(col - self.canvas.cols - 1)
        self._extend(1)

    def _render_emptyline(self):
        for m in self.modules:
            m.drawpipe(self.canvas, self.row)

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

        # Modules
        # columns
        self._render_modules()
