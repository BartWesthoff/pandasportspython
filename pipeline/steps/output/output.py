"""
abstract output class
inherited by every embedder
"""

from pipeline.steps.step import Step

# moet nog gedaan worden
class Output(Step):

    def __init__(self):
        super().__init__(Output)

    def process(self, data):
        pass
