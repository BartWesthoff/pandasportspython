class Pipeline:
    # What is a Pipeline?
    # A Pipeline is a set of instructions
    def __init__(self, *steps: str) -> None:
        """
        :param pipeline: step objects
        :return: nothing
        """
        if steps == ():
            raise ValueError("Pipeline steps are not specified")
        self.steps = steps

    # process -> take some data, modify it, output some data
    def process(self, data): # nog onzeker over format van data
        """
        :param data:  1-d List of strings (queries)
        :return: list of tuples [(anomaly,id,query)]
        """

        for step in self.steps:
            data = step.process(data)
        return data
