import os
import random

import numpy as np
import tensorflow as tf
from keras import Sequential, Input
from keras.applications.densenet import layers
from keras.layers import Dense, Masking, Dropout, RepeatVector
from keras.layers import LSTM
from keras.models import Sequential, Model
from sklearn.model_selection import train_test_split

from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


class VideoTrainer(Step):
    """" Class for the video training step"""

    def process(self, data) -> list:
        """" process the data of the step """
        max_len = 0

        list_of_vids = [i for i in os.listdir(os.sep.join(['data', 'embedded'])) if not 'normalized' in i]
        random.shuffle(list_of_vids)
        if self.settings['amount'] <=0:
            list_of_vids = list_of_vids[:len(list_of_vids)]
        else:
            list_of_vids = list_of_vids[:self.settings['amount']]
        ### get maximum length (amount of frames) of all videos
        for i in list_of_vids:
            squat = Utils().openEmbedding(i)
            if len(squat) > max_len:
                max_len = len(squat)
            # print(squat.shape)

        squats = np.array([Utils().openEmbedding(i) for i in list_of_vids])
        padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(
            squats, padding="post", value=-44
        )
        # pad all videos with zeros to the same length
        # for i in list_of_vids:
        #     squat = Utils().openEmbedding(i)
        #     squat = np.pad(squat, ((0, max_len - len(squat)), (0, 0)), 'constant', constant_values=0)
        #     # x = np.asarray(sq).astype('float32')
        #     padded_inputs.append(squat)

        # print(padded.shape)
        # padded_inputs = np.array(padded_inputs)
        # print(padded_inputs[0])

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

        # print(X_train[0])
        create_model = False
        lstm_ae = None
        random.seed(42)
        # masking_layer = Masking(mask_value=-44, input_shape=X_train.shape[1:])
        if create_model:
            time_steps = max_len
            n_features = 30
            input_layer = Input(shape=X_train.shape[1:])
            # I want to mask the timestep where all the feature values are 1 (usually we pad by 0)
            x = layers.Masking(mask_value=-44)(input_layer)
            x = LSTM(256, return_sequences=True)(x)
            x = Dropout(0.5)(x)
            x = LSTM(256, return_sequences=False)(x)
            x = Dropout(0.5)(x)
            x = layers.Dense(256, activation='relu')(x)
            x = layers.Dense(1, activation='sigmoid')(x)
            lstm_ae = Model(inputs=input_layer, outputs=x)
            lstm_ae.compile(optimizer='adam', loss='mse')
            print(lstm_ae.summary())
            lstm_ae.fit(X_train, y_train, epochs=20, validation_data=(X_val, y_val), batch_size=4)

            lstm_ae.save('lstm_ae.h5')
        # unmasked_embedding = tf.cast(
        #     tf.tile(tf.expand_dims(padded_inputs[:3], axis=-1), [1, 1, max_len, 30]), tf.float32
        # )

        # masked_embedding = masking_layer(unmasked_embedding)
        # print(masked_embedding._keras_mask)
        return [X_val, y_val, lstm_ae]


