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

    def process(self, data: dict) -> None:
        """Process the data of the step"""
        self.evaluate(data)

    def evaluate(self, data: dict) -> None:
        """Evaluates the model outcomes and classifying the results"""
        print("Evaluation")

        y_true = data["y_true"]
        y_pred = data["y_pred"]
        print(y_pred)
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
        zipped = zip(x, y_true, y_pred)

        # create scatter plot with a red dot if the prediction is correct and green if it is wrong
        list_good_index = []
        list_bad_index = []
        list_bad_prediction = []
        list_good_prediction = []
        for i in zipped:

            if i[1] == int(i[2] > 0.5):
                list_good_index.append(i[0])
                list_good_prediction.append(i[2])
            else:
                list_bad_index.append(i[0])
                list_bad_prediction.append(i[2])
        ax1.scatter(list_bad_index, list_bad_prediction, c="red", label="Wrong predicted labels")
        ax1.scatter(list_good_index, list_good_prediction, c="green", label="Correct predicted labels")
        ax1.scatter(x, [0.5 for _ in x], linewidths=0.5, color="black", alpha=0.3, marker="_")
        ax1.set_title('Predicted y values')
        ax1.set_xlabel('index')
        ax1.set_ylabel('Predicted y value')
        ax1.legend()
        f.tight_layout()
        f.show()
        plt.show()
