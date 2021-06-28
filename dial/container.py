class Container(list):
    def __init__(self, *args, **kwargs):
        # Wont's pass the args to the list due the brython bug.
        super().__init__()
