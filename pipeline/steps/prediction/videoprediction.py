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
        print("Percent correctly guessed:", self.correlationChecker(data[1], y_pred))
        #print(y_pred)
        y_pred = [1 if i > 0.7 else 0 for i in y_pred]
        y_true = data[1]

        return [y_pred, y_true]

    def correlationChecker(self, labels, y_pred):
        """Evaluates the model outcomes by finding a middleground between the lowest and highest score and classifying the results on that boundary"""
        y_pred_sorted = y_pred.copy()
        y_pred_sorted.sort()
        #print(y_pred_sorted)
        lowest = y_pred_sorted[0]
        highest = y_pred_sorted[-1]
        avg = (lowest + highest) / 2
        y_pred = [1 if i > avg else 0 for i in y_pred]
        correct_results = [1 if y_pred[i] == labels[i] else 0 for i in range(len(y_pred))]
        percent_correct = sum(correct_results) / len(correct_results)
        return percent_correct
