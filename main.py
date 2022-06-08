import os

from tensorflow import keras

from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.steps.prediction.videoprediction import VideoPrediction
from pipeline.steps.training.videotraining import VideoTrainer
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    # model = keras.models.load_model('RNN_model6627.h5')
    # pipeline = Pipeline(steps=[GoogleDriveService(),  MPEmbedder(), VideoTrainer(),VideoPrediction()], model=model)
    # pipeline.process()

    squat = Utils().openEmbedding('negative_squat_1')
    print(squat.shape)
    newsquats = Utils().augmentation(squat,save=True)

