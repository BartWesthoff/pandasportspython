"""
abstract model class
inherited by every model
"""

""""
NOTE: Model is not a step!! define self.__class__ == Model again!!
"""


class Model:
    def __init__(self, model):
        if self.__class__ == Model:
            raise Exception('I am abstract!')
        self.model = model

    def fit(self, x_train, y_train):
        pass

    @property
    def name(self):
        return self.__class__.__name__

    def predict(self, x_test):
        pass
