from abc import ABC, abstractmethod, abstractproperty

"""
steps sub-classes must implement method process
"""


class Step(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def process(self, X):
        pass