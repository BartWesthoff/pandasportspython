"""
abstract model class
inherited by every model
"""

""""
NOTE: Model is not a step!! define self.__class__ == Model again!!
"""


class Model:
    def __init__(self, model_specific, **model_kwargs):
        if self.__class__ == Model:
            raise Exception('I am abstract!')
        self.model_kwargs = model_kwargs
        self.model_specific = model_specific

    def fit(self, x_train, y_train):
        pass
