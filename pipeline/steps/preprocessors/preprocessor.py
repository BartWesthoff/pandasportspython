from pipeline.steps.step import Step

"""
abstract preprocessor class
inherited by every preprocessor class
"""


class PreProcessor(Step):

    def __init__(self):
        super().__init__(PreProcessor)

    def process(self, data):
        pass
