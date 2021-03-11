from abc import ABCMeta, abstractmethod
from collections.abc import Callable

class BasePipeline(metaclass=ABCMeta):
    
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



class BaseOperator(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass



class BaseModel(metaclass=ABCMeta):

    @abstractmethod
    def load_architecture(self):
        pass
    
    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self):
        pass




