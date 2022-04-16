from pipeline.steps.input.input import Input


class Pipeline:
    # What is a Pipeline?
    # A Pipeline is a set of instructions
    def __init__(self, *steps):
        """
        :param pipeline: step objects
        :return: nothing
        """
        if steps == ():
            raise ValueError("Pipeline steps are not specified")
        self.steps = steps

    # process -> take some data, modify it, output some data
    def process(self):
        """
        :param data:  1-d List of strings (queries)
        :return: list of tuples [(anomaly,id,query)]
        """
        data = None

        # if first item in array is not of type step
        if not isinstance(self.steps[0], Input):
            raise ValueError("First step must be Input")
        for step in self.steps:
            if type(step) == type(Input):
                data = step.process()
            else:
                data = step.process(data)
        return data
