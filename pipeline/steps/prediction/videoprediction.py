"""
PreProcessor class
used to preprocess video material
"""
import random as rnd

import numpy as np

from pipeline.steps.step import Step


class VideoPrediction(Step):
    """" Class for the video prediction step"""

    def process(self, data): # validation data
        """ process the data of the step """
        # print(predict_squat.shape)

        # print(padded.shape)
        # print(x_train[0].shape)
        # TODO vraag tony waarom reshape?
        # predict_squat = predict_squat.reshape(predict_squat.shape[0], predict_squat.shape[1], 1)
        model = data[2]
        if data[2] is None:
            model = self.model
        test = model.predict(data[0])
        print(test)
        print(data[1])
