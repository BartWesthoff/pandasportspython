from pipeline.steps.input.input import Input
from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


class Pipeline:
    # What is a Pipeline?
    # A Pipeline is a set of instructions
    def __init__(self, steps: list[Step], model) -> None:
        """ Instantiate the Pipeline class by recieving a list of steps """
        if steps == ():
            raise ValueError("Pipeline steps are not specified")
        self.steps = steps
        self.model = model
        Utils().save_current_model(model)

    # process -> take some data, modify it, output some data
    def process(self) -> object | None:  # nog onzeker over format van data
        """
        :param data:  1-d List of strings (queries)
        :return: list of tuples [(anomaly,id,query)]
        """
        data = None

        # if first item in array is not of type step
        if not isinstance(self.steps[0], Input):
            raise ValueError("First step must be Input")

        for step in self.steps:
            if issubclass(type(step), Input):
                data = step.process()
            else:
                print("Processing step: " + step.name)
                step.model = self.model
                data = step.process(data=data)
        return data
