from pipeline.steps.evaluation.evaluation import Evaluation
from pipeline.steps.preprocessors.preprocessor import PreProcessor


"""
Evaluation class
used to evaluate model performance
"""


class VideoEvaluation(Evaluation):

    def process(self, data):
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
