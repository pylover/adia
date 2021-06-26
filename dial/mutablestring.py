class MutableString(list):

    def __init__(self, initial):
        if isinstance(initial, str):
            self.length = len(initial)
            self.extend(initial)
        else:
            self.length = initial
            self.extend(' ' * initial)

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other

        return super().__eq__(other)

    def __ne__(self, other):
        if isinstance(other, str):
            return str(self) != other

        return super().__ne__(other)

    def __repr__(self):
        return f'\'{"".join(self)}\''

    def __str__(self):
        return ''.join(self)

    def __getitem__(self, s):
        return ''.join(super().__getitem__(s))

    def __setitem__(self, s, value):
        if isinstance(s, slice):
            vlen = len(value)
            stop = s.start + vlen
            if s.stop is None:
                s = slice(s.start, stop)

            elif s.stop > vlen:
                raise ValueError(
                    f'attempt to assign sequence of size {vlen} to replace '
                    f'with slice of size {s.stop - s.start}'
                )
        return super().__setitem__(s, value)
