import matplotlib.pyplot as plt
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
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
        # print(y_true)
        # total positive and negative examples
        total_positive = sum(y_true)
        total_negative = len(y_true) - total_positive
        print("Total positive:", total_positive)
        print("Total negative:", total_negative)
        # print(y_pred)
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        specificity = tn / (tn + fp)
        precision = precision_score(y_true, y_pred)
        accuracy = accuracy_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        print(f"precision: {precision}")
        print(f"accuracy: {accuracy}")
        print(f"recall: {recall}")
        print(f"f1: {f1}")
        print(f"specificity: {specificity}")

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
