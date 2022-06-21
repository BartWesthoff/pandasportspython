import os
import random

import numpy as np
import tensorflow as tf
from keras.applications.densenet import layers
from keras.layers import Masking
from tensorflow import keras

from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.dropboxservice import DropBoxService
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.steps.prediction.videoprediction import VideoPrediction
from pipeline.steps.training.videotraining import VideoTrainer
from pipeline.pipeline import Pipeline
from pipeline.utils.utils import Utils
from keras.models import Sequential
from keras.layers import LSTM, Dense, TimeDistributed
if __name__ == "__main__":
    pipeline = Pipeline(
        steps=[GoogleDriveService(), MPEmbedder(), VideoTrainer(), VideoPrediction(), VideoEvaluation()], model=None)
    pipeline.process()
# model = Sequential()
#
# model.add(LSTM(32, return_sequences=True, input_shape=(None,30)))
# model.add(LSTM(8))
# model.add(Dense(1, activation='sigmoid'))
#
# print(model.summary(90))
#
#
# allsquats = []
# for squat in os.listdir(os.sep.join(['data', 'embedded'])):
#     if 'normalized' in squat:
#         continue
#     else:
#         squat_embed = Utils().openEmbedding(squat)
#         # print(squat_embed.shape)
#         if squat_embed.shape[1] == 30:
#             # squat_embed = squat_embed[:90]
#             allsquats.append(squat)
# # print(np.array(allsquats).shape)
#
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# squat = Utils().openEmbedding('positive_squat_80')
#
# # print(allsquats[-120].shape == allsquats[0].shape)
# def train_generator():
#     for squat_name in allsquats:
#         x_train = Utils().openEmbedding(squat_name)
#         y_train = np.array([0 if 'negative' in squat_name else 1])
#         yield np.array([x_train]), y_train
#
#
# epochs=2
# steps_per_epoch=len(allsquats) // epochs
# model.fit(train_generator(), steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=1)
#
# pred = model.predict(np.array([squat]))
# print(pred)
# # print(len(allsquats))
