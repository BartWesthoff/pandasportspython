from random import randint

import numpy as np
from keras import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential

from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


class VideoTrainer(Step):
    """" Class for the video training step"""

    def process(self, data: list) -> object:
        """" process the data of the step """
        model = self.model
        X = [np.array(Utils().generatePoseList(10, 10)).reshape(1, 900)[0] for _ in range(0, 40)]
        # X = [np.array(Utils().generatePoseList(10, 10)).flatten() for _ in range(0, 40)]
        # TODO kijken of het werkt
        y = [randint(0, 100) for _ in range(0, 40)]
        fitted_model = model.fit(X, y)
        Utils.saveObject(fitted_model, f"{self.settings['baseline_model']}_fitted")
        return data

    def process2(self):
        max_len = 0
        ### get maximum length (amount of frames) of all videos
        for i in range(43, 52 + 1):
            squat = Utils().openEmbedding(f'bart_squat_{i}')
            if len(squat) > max_len:
                max_len = len(squat)
            # print(squat.shape)
        padded_inputs = []

        # pad all videos with zeros to the same length
        for i in range(43, 52 + 1):
            squat = Utils().openEmbedding(f'bart_squat_{i}')
            padded = np.zeros((max_len, squat.shape[1]))
            padded_inputs.append(padded)
            # print(padded.shape)
        padded_inputs = np.array(padded_inputs)
        # print(padded_inputs.shape)

        # split the data in training and test data
        x_test, x_train = np.split(padded_inputs, 2)
        ## build a simple RNN model
        model_rnn = Sequential()
        model_rnn.add(LSTM(50, input_shape=x_train.shape[1:]))
        model_rnn.add(Dense(1, activation='sigmoid'))

        # most of the parameters come from the embedding layer
        model_rnn.summary()

        compile_params = {'loss': 'binary_crossentropy', 'metrics': ['accuracy']}

        model_rnn.compile(**compile_params)
        # %%

        # LET OP: labels zijn fictief!!
        test_labels = np.array([0, 0, 1, 0, 1])
        train_labels = np.array([0, 0, 1, 0, 1])
        fit_params = {'batch_size': 2, 'epochs': 2, 'validation_data': (x_test, test_labels)}
        model_rnn.fit(x_train, train_labels, **fit_params)

        # predict op squat die nog niet gezien is door model
        predict_squat = Utils().openEmbedding(f'20220330_111746_Trim2')
        # print(predict_squat.shape)
        padded = np.zeros((max_len, predict_squat.shape[1]))
        # print(padded.shape)
        # print(x_train[0].shape)
        # TODO vraag tony waarom reshape?
        test_data = np.reshape(padded, (1, 667, 30))

        test = model_rnn.predict(test_data)
        print(test)

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
