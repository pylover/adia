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

    def draw_hline(self, row, startcol, length):
        for c in range(startcol, startcol + length):
            self._backend[row][c] = '-'

    def draw_box(self, col, row, width, height):
        lastrow = row + height - 1
        lastcol = col + width - 1
        hline_start = col + 1
        hline_end = width - 2
        vline_start = row + 1
        vline_end = height - 2

        self.draw_hline(row, hline_start, hline_end)
        self.draw_hline(lastrow, hline_start, hline_end)
        self.draw_vline(col, vline_start, vline_end)
        self.draw_vline(lastcol, vline_start, vline_end)
        self._backend[row][col] = '+'
        self._backend[row][col + width - 1] = '+'
        self._backend[row + height - 1][col] = '+'
        self._backend[row + height - 1][col + width - 1] = '+'

    def draw_line(self, col, row, line):
        self._backend[row][col:] = line

    def draw_text(self, col, row, text):
        for line in text.splitlines():
            self.draw_line(col, row, line)
            row += 1

    def draw_textbox(self, col, row, text, hmargin=0, vmargin=0):
        lines = text.splitlines()
        textheight = len(lines)
        width = max(len(l) for l in lines)

        boxheight = textheight + (vmargin * 2) + 2
        boxwidth = width + (hmargin * 2) + 2
        self.draw_text(col + hmargin + 1, row + vmargin + 1, text)
        self.draw_box(col, row, boxwidth, boxheight)
