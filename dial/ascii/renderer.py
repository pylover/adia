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
    pass


class ASCIISequenceRenderer(ASCIIRenderer):

    # Sequence
    def _render_modules(self):
        if not self.diagram.modules_order:
            return

        gutter = 1
        col = gutter
        self._extend(1)
        row = self.row
        for m in self.diagram.modules_order:
            t = self.diagram.modules[m].title
            lpad = 1
            rpad = 1 if len(t) % 2 else 2
            self.canvas.draw_textbox(col, row, t, hpadding=(lpad, rpad))
            col += gutter + len(t) + lpad + rpad + 2

        self.canvas.extendright(gutter)

    def render(self):
        # Sequence Header
        if self.diagram.title:
            self._extend(1)
            self.canvas.write_textline(
                1, self.row, f'SEQUENCE: {self.diagram.title} ')
            self._extend(1)

        self._render_modules()
        # Modules
        # columns
