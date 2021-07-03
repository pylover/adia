import abc


class Renderer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def render(self, diagram, canvas):
        raise NotImplementedError()
