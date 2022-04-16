from pipeline.steps.output.output import Output

"""
Output class
used to output the results of the training
"""


class VideoTraining(Output):

    def process(self, data):
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        # self.dosomething(data)
        # model denk ik gewoon ophalen van models folder
        # ik denk dat data lezen wordt vanaf het mapje waar de videos inzitten
        # output zal een getrained model zijn

        return data

    def plot(self, data):
        pass
