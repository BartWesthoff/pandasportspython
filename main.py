import os

import numpy as np

from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.steps.prediction.videoprediction import VideoPrediction
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotraining import VideoTrainer
import tensorflow as tf
import cv2
import numpy as np
from pipeline.utils.utils import Utils


if __name__ == "__main__":
    # model = tf.keras.models.load_model("model.h5")
    pipeline = Pipeline(
        steps=[GoogleDriveService(), VideoPreProcessor(), MPEmbedder(), VideoTrainer(), VideoPrediction(),
               VideoEvaluation()], model=None)
    pipeline.process()

    # for i in os.listdir(os.sep.join(["data", "embedded"])):
    #     if "normalized" in i:
    #         squat = Utils().openEmbedding(i)
    #         squats = Utils().data_augmentation_normalized(amount=10, name=i, squat=squat, save=True)
    #         print(squats.shape)


