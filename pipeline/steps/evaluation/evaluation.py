from pipeline.steps.step import Step

"""
abstract evaluation class
inherited by every evaluation class
"""


class Evaluation(Step):

    def __init__(self):
        super().__init__(Evaluation)

    def process(self, data):
        pass
