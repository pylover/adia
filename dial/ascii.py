from .mutablestring import MutableString


class ASCIICanvas:

    def __init__(self, cols, rows):
        self._backend = []
        for r in range(rows):
            self._backend.append(MutableString(cols))

    def __str__(self):
        return '\n'.join(str(l) for l in self._backend)

    def draw_vline(self, col, startrow, length):
        for r in range(startrow, startrow + length):
            self._backend[r][col] = '|'

    def write_hcenter(self, col, row, width, text):
        tlen = len(text)
        col = col + width // 2 - tlen // 2
        self.write_textline(col, row, text)

    def draw_hline(self, col, row, length, text=None, texttop=None,
                   textbottom=None):
        for c in range(col, col + length):
            self._backend[row][c] = '-'

        if text:
            self.write_hcenter(col, row, length, text)

        if texttop:
            self.write_hcenter(col, row - 1, length, texttop)

        if textbottom:
            self.write_hcenter(col, row + 1, length, textbottom)

    def draw_box(self, col, row, width, height):
        lastrow = row + height - 1
        lastcol = col + width - 1
        hline_start = col + 1
        hline_end = width - 2
        vline_start = row + 1
        vline_end = height - 2

        self.draw_hline(hline_start, row, hline_end)
        self.draw_hline(hline_start, lastrow, hline_end)
        self.draw_vline(col, vline_start, vline_end)
        self.draw_vline(lastcol, vline_start, vline_end)
        self._backend[row][col] = '+'
        self._backend[row][col + width - 1] = '+'
        self._backend[row + height - 1][col] = '+'
        self._backend[row + height - 1][col + width - 1] = '+'

    def write_textline(self, col, row, line):
        self._backend[row][col:] = line

    def write_textblock(self, col, row, text):
        for line in text.splitlines():
            self.write_textline(col, row, line)
            row += 1

    def draw_textbox(self, col, row, text, hmargin=0, vmargin=0):
        lines = text.splitlines()
        textheight = len(lines)
        width = max(len(l) for l in lines)

        boxheight = textheight + (vmargin * 2) + 2
        boxwidth = width + (hmargin * 2) + 2
        self.write_textblock(col + hmargin + 1, row + vmargin + 1, text)
        self.draw_box(col, row, boxwidth, boxheight)

    def draw_rightarrow(self, col, row, length, **kw):
        self.draw_hline(col, row, length - 1, **kw)
        self._backend[row][col + length - 1] = '>'

    def draw_leftarrow(self, col, row, length, **kw):
        self.draw_hline(col + 1, row, length - 1, **kw)
        self._backend[row][col] = '<'

    def draw_toparrow(self, col, row, length, **kw):
        self.draw_vline(col, row + 1, length - 1, **kw)
        self._backend[row][col] = '^'

    def draw_bottomarrow(self, col, row, length, **kw):
        self.draw_vline(col, row, length - 1, **kw)
        self._backend[row + length - 1][col] = 'v'
