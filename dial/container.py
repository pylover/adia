class Container(list):
    def __init__(self, *args, **kwargs):
        # FIXME: Wont's pass the args to the list due the brython bug:
        # https://github.com/brython-dev/brython/issues/1715
        # super().__init__(*args, **kwargs)
        super().__init__()
