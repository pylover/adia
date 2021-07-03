from ..renderer import Renderer
from ..sequence import SequenceDiagram

from .canvas import ASCIICanvas


class ASCIIRenderer(Renderer):
    def __init__(self, diagram):
        self.diagram = diagram
        self.canvas = ASCIICanvas()

    def _extend(self, i):
        self.canvas.extendbottom(i)

    @property
    def row(self):
        return self.canvas.rows - 1

    def render(self):
        self._render_header()

        for unit in self.diagram:
            if isinstance(unit, SequenceDiagram):
                self._render_sequence(unit)

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

    # Sequence
    def _render_sequencemodules(self, dia):
        if not dia.modules_order:
            return

        gutter = 1
        col = gutter
        self._extend(1)
        row = self.row
        for m in dia.modules_order:
            t = dia.modules[m].title
            lpad = 1
            rpad = 1 if len(t) % 2 else 2
            self.canvas.draw_textbox(col, row, t, hpadding=(lpad, rpad))
            col += gutter + len(t) + lpad + rpad + 2

        self.canvas.extendright(gutter)

    def _render_sequence(self, dia):
        # Sequence Header
        if dia.title:
            self._extend(1)
            self.canvas.write_textline(1, self.row, f'SEQUENCE: {dia.title} ')
            self._extend(1)

        self._render_sequencemodules(dia)
        # Modules
        # columns
