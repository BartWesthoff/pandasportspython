from pipeline.steps.input.input import Input
from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


class Pipeline:
    # What is a Pipeline?
    # A Pipeline is a set of instructions
    def __init__(self, steps: list[Step], model=None) -> None:
        """ Instantiate the Pipeline class by recieving a list of steps """
        if steps == ():
            raise ValueError("Pipeline steps are not specified")
        self.steps = steps
        self.model = model

    # process -> take some data, modify it, output some data
    def process(self) -> object | None:  # nog onzeker over format van data
        """ Process the data of the pipeline so that it can be used by the next step """
        data = None

        Utils.checkdirectories()
        for step in self.steps:
            if issubclass(type(step), Input):
                data = step.process()

            else:
                print("Processing step: " + step.name)
                step.model = self.model
                data = step.process(data=data)
        return data
