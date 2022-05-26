from pipeline.steps.step import Step

"""
Evaluation class
used to evaluate model performance
"""


class VideoEvaluation(Step):

    def process(self, data) -> None:
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        # data is hier een getrained model die moet gaan prediten
        # hier komt dus een metrics uit of plot
        # geeft momenteel niets terug
        self.evaluate(data)

        return data

    def evaluate(self, data):
        pass
