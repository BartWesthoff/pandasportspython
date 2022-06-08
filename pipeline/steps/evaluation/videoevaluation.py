from pipeline.steps.step import Step
from pipeline.utils.utils import Utils
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


    def evaluate(self, data: list[object, list[int]]) -> None:
        print(data)
        print("Evaluation")
