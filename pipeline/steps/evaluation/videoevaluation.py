from pipeline.steps.step import Step
from pipeline.utils.utils import Utils
import matplotlib.pyplot as plt
"""
Evaluation class
used to evaluate model performance
"""


class VideoEvaluation(Step):

    def process(self, data: list[object, list[int]]) -> None:
        # data is hier predicted labels
        # hier komt dus een metrics uit of plot
        # TODO: Hoe moeten we de echte labels erbij hebben?
        # TODO: als model beter is dan vorige opslaan

        Is_better = True
        if Is_better:
            print("Better model found!")
            # Utils.saveObject(data[0], f"{self.settings['baseline_model']}_best")
        self.evaluate(data)


    def evaluate(self, data: list[list[int]]) -> None:
        print(data)
        print("Evaluation")

        import seaborn as sns
        from sklearn.metrics import confusion_matrix
        y_true = data[1]
        y_pred = data[0]
        cm = confusion_matrix(y_true, y_pred)
        f = sns.heatmap(cm, annot=True, fmt='d')
        f.set_xlabel('Predicted labels')
        f.set_ylabel('True labels')
        f.set_title('Confusion matrix')
        plt.show()
