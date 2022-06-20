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

if __name__ == "__main__":
    random.seed(42)
    model = keras.models.load_model('lstm_ae.h5')
    # squat1 = Utils().openEmbedding('positive_squat_1')
    # squat2 = Utils().openEmbedding('positive_squat_2')
    # squat3 = Utils().openEmbedding('positive_squat_3')
    # squat1 = np.pad(squat1, ((0, 368 - len(squat1)), (0, 0)), 'constant', constant_values=-44)
    # print(squat1.shape)
    # out = model.predict([squat1])

    pipeline = Pipeline(
        steps=[GoogleDriveService(), MPEmbedder(), VideoTrainer(), VideoPrediction(), VideoEvaluation()], model=model)
    pipeline.process()

    # VideoEvaluation().process(None)
    #
    # squat1 = Utils().openEmbedding('positive_squat_1')
    # squat2 = Utils().openEmbedding('positive_squat_2')
    # squat3 = Utils().openEmbedding('positive_squat_3')
    # raw_inputs = [
    #     squat1,
    #     squat2,
    #     squat3
    # ]
    # max_len = 0
    # list_of_vids = [i for i in os.listdir(os.sep.join(['data', 'embedded'])) if not 'normalized' in i]
    # random.shuffle(list_of_vids)
    # list_of_vids = list_of_vids[:3]
    # ### get maximum length (amount of frames) of all videos
    # for i in list_of_vids:
    #     squat = Utils().openEmbedding(i)
    #     if len(squat) > max_len:
    #         max_len = len(squat)
    #     # print(squat.shape)
    #
    #
    # squats = np.array([Utils().openEmbedding(i) for i in list_of_vids])
    # print(squats.shape)
    #
    # # By default, this will pad using 0s; it is configurable via the
    # # "value" parameter.
    # # Note that you could use "pre" padding (at the beginning) or
    # # "post" padding (at the end).
    # # We recommend using "post" padding when working with RNN layers
    # # (in order to be able to use the
    # # CuDNN implementation of the layers).
    # padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(
    #     squats, padding="post",value=-44
    # )
    #
    # masking_layer = layers.Masking(mask_value=-44)
    # # Simulate the embedding lookup by expanding the 2D input to 3D,
    # # with embedding dimension of 10.
    # unmasked_embedding = tf.cast(
    #     tf.tile(tf.expand_dims(padded_inputs, axis=-1), [1,1, max_len, 30]), tf.float32
    # )
    #
    # masked_embedding = masking_layer(unmasked_embedding)
    # print(masked_embedding._keras_mask)
    #
    #
    #
    #
