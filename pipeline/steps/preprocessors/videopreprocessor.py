import os

from pipeline.steps.preprocessors.preprocessor import PreProcessor
from pipeline.utils.utils import Utils

"""
PreProcessor class
used to preprocess video material
"""


class VideoPreProcessor(PreProcessor):

    def process(self, data):
        """
        :param data: 1-d List of Strings
        :return: dictionary of 1-d List of Strings (but even spaced so they can be inferred correctly)
            and original queries
        """
        self._preprocessVideo(data)

        return

    def _preprocessVideo(self, data):
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
                destination = folder + f"{name}_squat{index // 2}.mp4"

                # destination = folder.replace(f'{name}_squat', "production") + f"{name}_squat{index}.mp4"

                # Video bestaat al zonder geluid
                if not os.path.exists(destination):
                    os.rename(source, destination)
                    Utils().removesound(str(destination))
