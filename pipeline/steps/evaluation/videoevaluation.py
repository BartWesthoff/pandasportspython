from pipeline.steps.step import Step

"""
Evaluation class
used to evaluate model performance
"""


class VideoEvaluation(Step):

    def process(self, data) -> None:
        # data is hier een getrained model die moet gaan prediten
        # hier komt dus een metrics uit of plot
        # geeft momenteel niets terug
        self.evaluate(data)

        return data

    def evaluate(self, data):
        pass
