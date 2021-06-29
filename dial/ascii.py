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

#     def draw_text(self, col, row, text):
