from pipeline.steps.step import Step


class Embedder(Step):
    """ Abstract class for a embedding step"""

    def __init__(self):
        super().__init__()

    def embed(self, video) -> list[list[int]] | object:
        """ Embeds the data """
        pass

    def process(self, data) -> object:
        """ Process data """
        pass

