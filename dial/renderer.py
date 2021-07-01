import abc


class Canvas(metaclass=abc.ABCMeta):
    pass


class Renderer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def render(self, diagram, canvas):
        raise NotImplementedError()
