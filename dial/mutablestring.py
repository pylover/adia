class MutableString:
    """A simple wrapper arround a list of str."""

    def __init__(self, initial):
        self._backend = []

        if isinstance(initial, str):
            self += initial
        else:
            self.extendright(initial)

    def __iadd__(self, new):
        self._backend.extend(new)
        return self

    def __len__(self):
        return self._backend.__len__()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.__str__() == other

        return self._backend == other

    def __ne__(self, other):
        if isinstance(other, str):
            return self.__str__() != other

        return self._backend != other

    def __str__(self):
        return ''.join(self._backend)

    def __repr__(self):
        return f'\'{self.__str__()}\''

    def __getitem__(self, s):
        return ''.join(self._backend.__getitem__(s))

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
        return self._backend.__setitem__(s, value)

    def __delitem__(self, s):
        self._backend.__delitem__(s)

    def reverse(self):
        self._backend.reverse()

    def insert(self, index, s):
        for i in s[::-1]:
            self._backend.insert(index, i)

    def extendright(self, size):
        self._backend.extend(' ' * size)

    def extendleft(self, size):
        while size:
            self._backend.insert(0, ' ')
            size -= 1

    def _trim(self, size, index=-1):
        while size:
            self._backend.pop(index)
            size -= 1

    def trimstart(self, size):
        self._trim(size, index=0)

    def trimend(self, size):
        self._trim(size)
