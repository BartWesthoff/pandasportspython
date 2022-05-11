"""
abstract embedders class
inherited by every embedder
"""

from pipeline.steps.step import Step

from typing import Set

class Embedder(Step):

    def __init__(self)->None:
        super().__init__(Embedder)

    def process(self, data)->None:
        pass
