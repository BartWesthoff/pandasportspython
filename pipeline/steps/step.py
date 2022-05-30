from abc import ABC, abstractmethod

import yaml

"""
step sub-classes must implement method process
"""


class Step(ABC):

    def __init__(self, class_type=None):
        """ Instantiate the Step class """
        # NOTE: issubclass(self.__class__, type) werkt niet
        if self.__class__ == class_type:
            raise Exception('I am abstract!')

    @property
    def name(self) -> str:
        """ Return the name of the step """
        return self.__class__.__name__

    @abstractmethod
    def process(self, data) -> object:
        """abstract method for using the data of the step."""
        pass

    @property
    def settings(self) -> dict:
        """" Return the settings of the step """
        with open("settings.yaml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data["settings"]
