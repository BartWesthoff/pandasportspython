"""
PreProcessor class
used to preprocess video material
"""
from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


# Klasse voor VideoPrediction
class VideoPrediction(Step):

    def process(self, data):
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        # voorbeeld data np.array(Utils().generatePoseList(10, 10)).reshape(1, 900))[0]][0]
        model = Utils.openObject(self.settings['model_name'])
        model.predict(data)

        # eventueel voting classifier gebruiken
        return data
