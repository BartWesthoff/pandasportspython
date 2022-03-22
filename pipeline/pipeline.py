class Pipeline:
    # What is a Pipeline?
    def __init__(self, *steps):
        """
        :param pipeline: step objects
        :return: nothing
        """
        if steps == ():
            raise ValueError("Pipeline steps are not specified")
        self.steps = steps

    # process -> take some data, modify it, output some data
    def process(self,data):
        """
        :param data:  1-d List of strings (queries)
        :return: list of tuples [(anomaly,id,query)]
        """


        for step in self.steps:
            data = step.process(data)
        return data