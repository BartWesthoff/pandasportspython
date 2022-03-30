"""
abstract embedders class
inherited by every embedder
"""

from pipeline.steps.step import Step


class Embedder(Step):

    def __init__(self):
        super().__init__(Embedder)

    def process(self, data):
        pass
