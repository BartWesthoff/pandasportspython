
"""
PreProcessor class
used to preprocess video material
"""
from pipeline.steps.step import Step


class VideoOutput(Step):

    def process(self, data):
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        #self.dosomething(data)
        # ik denk dat deze class overbodig is
        # we kunenn beter de statitische evaluation gebruiken als laatste stap
        # eventueel deployen van het model kan ook los van de pipeline
        print(data)
        return data

