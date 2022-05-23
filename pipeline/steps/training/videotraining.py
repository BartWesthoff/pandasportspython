import numpy as np

from pipeline.models.KNNmodel import SVMModel
from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


class VideoTrainer(Step):

    def process(self, data) -> object:
        model = SVMModel('')
        fitted_model = model.fit()
        Utils().saveObject(fitted_model, 'SVMmodel')
        return data

    # def process(self, data: list):
    #     """gets array of video's"""
    #     """return fitted model"""
    #     labels = []
    #     utils = Utils()
    #     allFiles = os.listdir(utils.datafolder)
    #
    #     for file in allFiles:
    #         kind = file.split('_')[0]
    #         if kind in ["positive", "negative"]:
    #             labels.append(kind)
    #         else:
    #             raise Exception("False names!")
    #
    #     if len(labels) != len(data):
    #         raise Exception("Length of data and labels do not match!")
    #     model = utils.define_model()
    #     data = np.array(data)
    #     data = np.reshape(data, (len(labels), 137, 99))
    #     fitted = model.fit(data, np.array(labels), epochs=2, batch_size=2, verbose=1)
    #     Utils.saveObject(fitted, "fittedSequentialTestModel")
    #     print(type(fitted))
    #     return fitted
