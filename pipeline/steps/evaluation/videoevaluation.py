import matplotlib.pyplot as plt
from sklearn.metrics import precision_score

from pipeline.steps.step import Step

"""
Evaluation class
used to evaluate model performance
"""
import seaborn as sns
from sklearn.metrics import confusion_matrix


class VideoEvaluation(Step):

    def process(self, data: list[list[int]]) -> None:
        # data is hier predicted labels
        # hier komt dus een metrics uit of plot
        # TODO: Hoe moeten we de echte labels erbij hebben?
        # TODO: als model beter is dan vorige opslaan
        self.evaluate(data)

    def evaluate(self, data: list[list[int]]) -> None:
        print("Evaluation")

        y_true = data[1]
        y_pred = data[0]
        print(y_true)
        print(y_pred)
        cm = confusion_matrix(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        print(precision)
        # save current model to name 'model_best.h5' if model is better
        is_better = False
        # TODO nog even kijken of model echt beter is en dan die opslaan
        if is_better:
            print("Better model found!")
            # Utils.saveObject(data[0], f"{self.settings["baseline_model"]}_best")

        f = sns.heatmap(cm, annot=True, fmt="d")
        f.set_xlabel("Predicted labels")
        f.set_ylabel("True labels")
        f.set_title("Confusion matrix")
        plt.show()
