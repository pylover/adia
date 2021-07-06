import abc


class Renderer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def dumps(self, diagram, canvas):
        raise NotImplementedError()
