from abc import ABCMeta, abstractmethod
from collections.abc import Callable

class PipeLineBase(metaclass=ABCMeta):
    
    @abstractmethod
    def run(self):
        pass
    

    @abstractmethod
    def remove_operator(self):
        pass


    @abstractmethod
    def add_operator(self):
        pass

    @abstractmethod
    def show_operator(self):
        pass


class OperatorBase(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass

