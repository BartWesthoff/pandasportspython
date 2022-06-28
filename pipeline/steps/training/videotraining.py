import os
import random

import numpy as np
import tensorflow as tf
from keras import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential

from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


# from sklearn.model_selection import train_test_split


class VideoTrainer(Step):
    """" Class for the video training step"""

    def process(self, data):  # TODO even nog checken wat ie teruggeeft
        """" process the data of the step """
        # For debugging. Eliminates any randomness from the program
        using_seed = True
        if using_seed:
            np.random.seed(69)
            random.seed(42)
            tf.random.set_seed(42)

        list_of_train_embeds = [i for i in os.listdir(os.sep.join(["data", "embedded"]))]
        if self.settings["normalize_landmarks"]:
            list_of_train_embeds = [i for i in list_of_train_embeds if "normalized" in i]

        random.shuffle(list_of_train_embeds)
        if self.settings["amount"] > 0:
            list_of_train_embeds = list_of_train_embeds[:self.settings["amount"]]

        list_of_test_embeds = [i for i in os.listdir(os.sep.join(["data", "testdata"]))]
        # if self.settings["normalize_landmarks"]:
        #     list_of_test_embeds = [i for i in list_of_test_embeds if "normalized" in i]

        random.shuffle(list_of_test_embeds)
        if self.settings["amount"] > 0:
            list_of_test_embeds = list_of_test_embeds[:self.settings["amount"]]




        # squats = np.array([Utils().openEmbedding(i) for i in list_of_vids], dtype=object)

        create_model = self.model is None
        model = None
        if create_model:
            model = Sequential()

            model.add(LSTM(4, input_shape=(None, 30)))
            model.add(Dense(1, activation="sigmoid"))

            print(model.summary(90))
            model.compile(loss="binary_crossentropy", optimizer="adam")
            epochs = 50
            steps_per_epoch = len(list_of_train_embeds) // epochs
            model.fit(self.train_generator(list_of_train_embeds), steps_per_epoch=steps_per_epoch, epochs=epochs,
                      verbose=1)
            model.save('baselinemodel42000NG9train.h5')
        labels = [1 if "positive" in i else 0 for i in list_of_test_embeds]
        print(f"amount of labels {len(labels)}")
        test_data = None
        if self.testdata is not None:
            test_data = [np.array([Utils().openTestEmbedding(i)]) for i in list_of_test_embeds]
        return test_data, np.array(labels), model

    def train_generator(self, listofvids):
        """Generates batches (1 piece) of data for training"""
        for squat_name in listofvids:
            x_train = Utils().openEmbedding(squat_name)
            y_train = np.array([0 if "negative" in squat_name else 1])
            yield np.array([x_train]), y_train
