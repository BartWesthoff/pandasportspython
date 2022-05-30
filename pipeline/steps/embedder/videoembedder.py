from pipeline.steps.step import Step


class Embedder(Step):

    def __init__(self):
        super().__init__()

    def embed(self, video) -> list[list[int]] | object:
        pass

    def process(self, data) -> object:
        pass

