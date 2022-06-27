import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

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
        y_pred_hard = [1 if i > 0.5 else 0 for i in y_pred]
        total_positive = sum(y_true)
        total_negative = len(y_true) - total_positive
        print("Total positive:", total_positive)
        print("Total negative:", total_negative)
        cm = confusion_matrix(y_true, y_pred_hard)
        tn, fp, fn, tp = cm.ravel()
        specificity = tn / (tn + fp)
        precision = precision_score(y_true, y_pred_hard)
        accuracy = accuracy_score(y_true, y_pred_hard)
        recall = recall_score(y_true, y_pred_hard)
        f1 = f1_score(y_true, y_pred_hard)

        print(f"precision: {precision}")
        print(f"accuracy: {accuracy}")
        print(f"recall: {recall}")
        print(f"f1: {f1}")
        print(f"specificity: {specificity}")

        x = [i for i in range(len(y_true))]

        f, (ax1, ax2) = plt.subplots(1, 2)
        ax2 = sns.heatmap(cm, annot=True, fmt="d")
        ax2.set_xlabel("Predicted labels")
        ax2.set_ylabel("Actual labels")
        ax2.set_title("Confusion matrix")

        zipped = zip(x, y_true, y_pred_hard)

        # create scatter plot with a red dot if the prediction is correct and green if it is wrong
        # for i in zipped:
        #     if i[1] == i[2]:
        #         ax1.scatter(i[0], i[1], color="red")
        #     else:
        #         ax1.scatter(i[0], i[1], color="green")
        #     print(i)
        ax1.scatter(x, y_pred, c=["green" if i[1] == i[2] else "red" for i in list(zipped)], label="Predicted labels")
        ax1.scatter(x, [0.5 for i in x], linewidths=0.5, color="black", label="Threshold", alpha=0.3, marker="_")
        ax1.set_title('Predicted y values')
        f.tight_layout()
        f.show()
        plt.show()
