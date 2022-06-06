from __future__ import print_function
from functools import reduce

import numpy as np
import tf
from keras.initializers.initializers_v1 import RandomNormal
from keras.initializers.initializers_v2 import Identity
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from keras.layers import SimpleRNN
from keras.datasets import imdb
from keras import Sequential
from keras.applications.densenet import layers
from keras.layers import Dense

from pipeline.steps.training.videotraining import VideoTrainer
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    # pipeline = Pipeline(steps=[GoogleDriveService(), MPEmbedder()], model=None)
    # pipeline.process()

    # max_len= 0
    # for i in range(43, 52+1):
    #     squat = Utils().openEmbedding(f'bart_squat_{i}')
    #     if len(squat) > max_len:
    #         max_len = len(squat)
    #     print(squat.shape)
    # padded_inputs = []
    # for i in range(43, 52+1):
    #     squat = Utils().openEmbedding(f'bart_squat_{i}')
    #     padded = np.zeros((max_len, squat.shape[1]))
    #     padded_inputs.append(padded)
    #     print(padded.shape)
    # padded_inputs = np.array(padded_inputs)
    # print(padded_inputs.shape)
    #
    # x_test, x_train =  np.split(padded_inputs, 2)
    # ## build a RNN
    # rnn_hidden_dim = 5
    # word_embedding_dim = 50
    #
    #
    # model_rnn = Sequential()
    # model_rnn.add(LSTM(50, input_shape=x_train.shape[1:]))
    # model_rnn.add(Dense(1, activation='sigmoid'))
    #
    # # most of the parameters come from the embedding layer
    # model_rnn.summary()
    #
    # compile_params = {'loss': 'binary_crossentropy',  'metrics': ['accuracy']}
    #
    # model_rnn.compile(**compile_params)
    # # %%
    # fit_params = {'batch_size': 2, 'epochs': 2, 'validation_data': (x_test, np.array([0,0,1,0,1]))}
    # model_rnn.fit(x_train, np.array([0,0,1,0,1]), **fit_params)
    #
    # predict_squat = Utils().openEmbedding(f'20220330_111746_Trim2')
    # print(predict_squat.shape)
    # padded = np.zeros((max_len, predict_squat.shape[1]))
    # print(padded.shape)
    # print(x_train[0].shape)
    # test_data = np.reshape(padded, (1, 667, 30))
    # # TODO vraag tony waarom reshape?
    # test = model_rnn.predict(test_data)
    # print(test)

    VideoTrainer().process2()