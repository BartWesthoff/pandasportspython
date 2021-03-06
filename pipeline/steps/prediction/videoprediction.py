"""
PreProcessor class
used to preprocess video material
"""
import os

import numpy as np

from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


class VideoPrediction(Step):
    """" Class for the video prediction step"""

    def process(self, data: dict) -> dict:
        """ process the data of the step """
        model = data["model"]

        if model is None:
            model = self.model
        data_to_predict = data["test_data"]
        y_true = data["labels"]
        if not self.settings["trainmode"]:
            data_to_predict = os.listdir(os.sep.join(["data", "embedded_test"]))
            y_true = [1 if "positive" in i else 0 for i in data_to_predict]

            data_to_predict = [np.array([Utils().openEmbedding(i, "embedded_test")]) for i in data_to_predict]

        y_pred = [model.predict(i) for i in data_to_predict]
        # correct, y_pred = self.correlationChecker(data[1], y_pred)
        results = {"y_true": y_true, "y_pred": y_pred}
        return results

    def correlationChecker(self, labels, y_pred):
        """ Evaluates the model outcomes by finding the average
        between the lowest and highest score and classifying the results on that boundary """
        y_pred_sorted = y_pred.copy()
        y_pred_sorted.sort()
        # print(y_pred_sorted)
        lowest = y_pred_sorted[0]
        highest = y_pred_sorted[-1]
        avg = (lowest + highest) / 2
        y_pred = [int(i > avg) for i in y_pred]
        correct_results = [y_pred[i] == labels[i] for i in range(len(y_pred))]
        percent_correct = sum(correct_results) / len(correct_results)
        return percent_correct, y_pred
