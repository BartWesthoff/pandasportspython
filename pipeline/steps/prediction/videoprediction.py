"""
PreProcessor class
used to preprocess video material
"""
from pipeline.steps.step import Step
from pipeline.utils.utils import Utils
from pipeline.models.model import Model

class VideoPrediction(Step):
    """" Class for the video prediction step"""

    def process(self, data: Model) -> list[Model, list[int]]:
        """
        :param data: n.t.b
        :return: predictions of data 1-d list of ints
        """
        # voorbeeld data np.array(Utils().generatePoseList(10, 10)).reshape(1, 900))[0]][0]
        model = Utils.openObject(f"{self.settings['baseline_model']}_fitted")
        prediction = model.predict(data)

        # eventueel voting classifier gebruiken
        return [model, prediction]
