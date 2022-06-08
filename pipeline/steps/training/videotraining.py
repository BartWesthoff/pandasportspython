import os
import random

import numpy as np
from keras import Sequential
from keras.layers import Dense, Embedding, Masking
from keras.layers import LSTM
from keras.models import Sequential
from sklearn.model_selection import train_test_split

from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


class VideoTrainer(Step):
    """" Class for the video training step"""

    def process(self, data) -> object:
        """" process the data of the step """
        max_len = 0

        list_of_vids = [i for i in os.listdir(os.sep.join(['data', 'embedded']))]
        random.shuffle(list_of_vids)
        ### get maximum length (amount of frames) of all videos
        for i in list_of_vids:
            squat = Utils().openEmbedding(i)
            if len(squat) > max_len:
                max_len = len(squat)
            # print(squat.shape)
        print(max_len)

        padded_inputs = []

        # pad all videos with zeros to the same length
        for i in list_of_vids:
            squat = Utils().openEmbedding(i)

            padded = np.pad(squat, ((0, max_len - len(squat)), (0, 0)), 'constant', constant_values=0)
            # padded = np.zeros((max_len, squat.shape[1]))
            padded_inputs.append(padded)

            # print(padded.shape)
        padded_inputs = np.array(padded_inputs)
        # print(padded_inputs[0])
        for i in padded_inputs[0]:
            print(i)
            print(len(i))
            print(type(i))
            if np.array_equal(i, np.zeros(len(i))):
            # if np.array_equal(i , np.array([0. for _ in range(30)])):
                print('found')

        # quit()
        # print(padded_inputs.shape)
        labels = np.array([])
        for i in list_of_vids:
            if 'positive' in i:
                labels = np.append(labels, 1)
            elif 'negative' in i:
                labels = np.append(labels, 0)

        # split the data in training and test data

        X_train, X_test, y_train, y_test = train_test_split(padded_inputs, labels, test_size=0.2)

        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25)  # 0.25 x 0.8 = 0.2

        ## build a simple RNN model
        create_model = False
        if create_model:
            print(X_train.shape[2])
            model_rnn = Sequential()
            model_rnn.add(Masking(mask_value=np.zeros(30),  input_shape=X_train.shape[1:]))
            model_rnn.add(LSTM(50, input_shape=X_train.shape[1:]))
            model_rnn.add(Dense(5, activation='sigmoid'))
            model_rnn.add(Dense(1, activation='sigmoid'))

            # most of the parameters come from the embedding layer
            model_rnn.summary()

            compile_params = {'loss': 'binary_crossentropy', 'metrics': ['accuracy']}

            model_rnn.compile(**compile_params)
            fit_params = {'batch_size': 2, 'epochs': 200, 'validation_data': (X_val, y_val)}
            model_rnn.fit(X_train, y_train, **fit_params)
            rnn_name = f"RNN_model{random.randint(0, 10000)}.h5"
            print(f"saved model {rnn_name}")
            model_rnn.save(rnn_name)
        return [X_test, y_test]
