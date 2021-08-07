from .mutablestring import MutableString


class Canvas:

    def __init__(self, size=(0, 0)):
        self._backend = []
        self.cols = size[0]
        self.rows = 0
        self.extendbottom(size[1])

    def __iter__(self):
        for line in self._backend:
            yield line

    @property
    def size(self):
        return self.cols, self.rows

    def extendright(self, addcols):
        assert addcols >= 0
        for r in self._backend:
            r.extendright(addcols)

        self.cols += addcols

    def extendleft(self, addcols):
        assert addcols >= 0
        for r in self._backend:
            r.extendleft(addcols)

        self.cols += addcols

    def extendbottom(self, addrows):
        assert addrows >= 0
        for i in range(addrows):
            self._backend.append(MutableString(self.cols))

        self.rows += addrows

    def extendtop(self, addrows):
        assert addrows >= 0
        for i in range(addrows):
            self._backend.insert(0, MutableString(self.cols))

        self.rows += addrows

    def __str__(self):
        return '\n'.join(str(line) for line in self._backend) + '\n'

    def set_char(self, col, row, char):
        if col >= self.cols:
            self.extendright((col + 1) - self.cols)

        if row >= self.rows:
            self.extendbottom((row + 1) - self.rows)

        self._backend[row][col] = char

    def draw_vline(self, col, startrow, length, char='|'):
        for r in range(startrow, startrow + length):
            self.set_char(col, r, char)

    def write_textline(self, col, row, line):
        for c in line:
            self.set_char(col, row, c)
            col += 1

    def write_hcenter(self, col, row, text, width=None):
        tlen = len(text)
        if tlen > self.cols:
            self.extendright(tlen - self.cols)

        col = col + (width or self.cols) // 2 - tlen // 2
        self.write_textline(col, row, text)

    def draw_hline(self, col, row, length, text=None, texttop=None,
                   textbottom=None, char='-'):
        for c in range(col, col + length):
            self.set_char(c, row, char)

        if text:
            self.write_hcenter(col, row, text, length)

        if texttop:
            self.write_hcenter(col, row - 1, texttop, length)

        if textbottom:
            self.write_hcenter(col, row + 1, textbottom, length)

    def draw_box(self, col, row, width, height, hlinechar='-', vlinechar='|',
                 cornerchar='+'):
        lastrow = row + height - 1
        lastcol = col + width - 1
        hline_start = col + 1
        hline_end = width - 2
        vline_start = row + 1
        vline_end = height - 2

        self.draw_hline(hline_start, row, hline_end, char=hlinechar)
        self.draw_hline(hline_start, lastrow, hline_end, char=hlinechar)
        self.draw_vline(col, vline_start, vline_end, char=vlinechar)
        self.draw_vline(lastcol, vline_start, vline_end, char=vlinechar)
        self.set_char(col, row, cornerchar)
        self.set_char(col + width - 1, row, cornerchar)
        self.set_char(col, row + height - 1, cornerchar)
        self.set_char(col + width - 1, row + height - 1, cornerchar)

    def write_textblock(self, col, row, text):
        for line in text.splitlines():
            self.write_textline(col, row, line)
            row += 1

    def draw_textbox(self, col, row, text, mincols=0, hpadding=0, vpadding=0,
                     **kw):
        lines = text.splitlines()
        textheight = len(lines)
        width = max(mincols, max(len(line) for line in lines))

        if not isinstance(hpadding, int):
            lpad, rpad = hpadding
        else:
            lpad = rpad = hpadding

        boxheight = textheight + (vpadding * 2) + 2
        boxwidth = width + lpad + rpad + 2
        self.write_textblock(col + lpad + 1, row + vpadding + 1, text)
        self.draw_box(col, row, boxwidth, boxheight, **kw)

    def draw_rightarrow(self, col, row, length, **kw):
        self.draw_hline(col, row, length - 1, **kw)
        self.set_char(col + length - 1, row, '>')

    def draw_leftarrow(self, col, row, length, **kw):
        self.draw_hline(col + 1, row, length - 1, **kw)
        self.set_char(col, row, '<')

    def draw_toparrow(self, col, row, length, **kw):
        self.draw_vline(col, row + 1, length - 1, **kw)
        self.set_char(col, row, '^')

    def draw_bottomarrow(self, col, row, length, **kw):
        self.draw_vline(col, row, length - 1, **kw)
        self.set_char(col, row + length - 1, 'v')
