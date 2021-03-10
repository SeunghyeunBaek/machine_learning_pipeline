from abc import ABCMeta, abstractmethod
from collections.abc import Callable

class PipeLineBase(metaclass=ABCMeta):
    
    @abstractmethod
    def run(self):
        pass
    

    @abstractmethod
    def remove_operation(self):
        pass


    @abstractmethod
    def add_operation(self):
        pass

    @abstractmethod
    def show_operation(self):
        pass


class OperationBase(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass

