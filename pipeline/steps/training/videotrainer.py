import os
import random

import numpy as np
import tensorflow as tf
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
from keras.optimizers import SGD

from pipeline.steps.step import Step
from pipeline.utils.utils import Utils


# from sklearn.model_selection import train_test_split


class VideoTrainer(Step):
    """" Class for the video training step"""

    def process(self, data: None) -> dict:  # TODO even nog checken wat ie teruggeeft
        """" process the data of the step """
        # For debugging. Eliminates any randomness from the program
        using_seed = True
        if using_seed:
            np.random.seed(69)
            random.seed(42)
            tf.random.set_seed(42)
        list_of_train_embeds = [i for i in os.listdir(os.sep.join(["data", "embedded"]))]
        random.shuffle(list_of_train_embeds)
        if self.settings["amount"] > 0:
            list_of_train_embeds = list_of_train_embeds[:self.settings["amount"]]

        list_of_test_embeds = [i for i in os.listdir(os.sep.join(["data", "testdata"]))]
        random.shuffle(list_of_test_embeds)
        if self.settings["amount"] > 0:
            list_of_test_embeds = list_of_test_embeds[:self.settings["amount"]]

        create_model = self.model is None
        model = None
        if create_model:
            model = Sequential([
                LSTM(12, input_shape=(None, 30), activation="relu"),
                Dense(1, activation="sigmoid")
            ])

            print(model.summary(90))
            model.compile(SGD(lr=0.003), "binary_crossentropy", metrics=["accuracy"])
            epochs = 2
            # if self.settings["amount"] < epochs:
            #     epochs = self.settings["amount"]
            steps_per_epoch = len(list_of_train_embeds) // epochs
            model.fit(self.train_generator(list_of_train_embeds), steps_per_epoch=steps_per_epoch, epochs=epochs,
                      verbose=1)
            model.save('testtrainmodel.h5')
        labels = [1 if "positive" in i else 0 for i in list_of_test_embeds]
        print(f"amount of labels {len(labels)}")
        test_data = None
        if self.settings["trainmode"] is not False:
            test_data = [np.array([Utils().openEmbedding(i, "testdata")]) for i in list_of_test_embeds]
        dictionary = {"test_data": test_data, "labels": np.array(labels), "model": model}
        return dictionary

    def train_generator(self, listofvids):
        """Generates batches (1 piece) of data for training"""
        for squat_name in listofvids:
            x_train = Utils().openEmbedding(squat_name, "embedded")
            y_train = np.array([0 if "negative" in squat_name else 1])
            yield np.array([x_train]), y_train
