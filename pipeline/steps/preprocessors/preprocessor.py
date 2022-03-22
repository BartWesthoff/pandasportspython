import os

from pipeline.utils.utils import Utils

from pipeline.steps.step import Step

import shutil


"""
abstract fitStep class
inherited by every fitStep class
"""

class PreProcessor(Step):

    def process(self):
        """
        :param X: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        self._preprocessVideo()

        return

    def _preprocessVideo(self):
        """
        :param query: string
        :return: modified string
        """


        for name in ["positive", "negative"]:
            folder = Utils().root_dir + os.sep + "data" + os.sep + f"{name}_squat" + os.sep
            for index, file_name in enumerate(os.listdir(folder)):
                # Construct old file name
                source = folder + file_name

                # Adding the count to the new file name and extension
                # TODO bespreken: hoe gaan we 'ready' data neerzetten?
                # met production data folder of gewoon overwritten
                destination = folder + f"{name}_squat{index//2}.mp4"

                # destination = folder.replace(f'{name}_squat', "production") + f"{name}_squat{index}.mp4"


                # Video bestaat al zonder geluid
                if not os.path.exists(destination):
                    os.rename(source, destination)
                    Utils().removesound(str(destination))
