from abc import ABC, abstractmethod

"""
step sub-classes must implement method process
"""


class Step(ABC):
    """" checks if class is instantiated"""
    def __init__(self, type):
        """ this has to be type because in a """
        """ inherented situation it will always become true """
        # NOTE: issubclass(self.__class__, type) werkt niet
        if self.__class__ == type:
            raise Exception('I am abstract!')

    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def process(self, data):
        pass
