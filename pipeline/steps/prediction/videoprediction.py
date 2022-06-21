"""
PreProcessor class
used to preprocess video material
"""

from pipeline.steps.step import Step


class VideoPrediction(Step):
    """" Class for the video prediction step"""

    def process(self, data):  # validation data
        """ process the data of the step """
        model = data[2]

        if data[2] is None:
            model = self.model
        y_pred = [model.predict(i) for i in data[0]]
        y_pred = [1 if i > 0.5 else 0 for i in y_pred]
        y_true = data[1]

        return [y_pred, y_true]
