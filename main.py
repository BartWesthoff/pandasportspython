import os
import pickle

import tensorflow as tf

from pipeline.pipeline import Pipeline
from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.steps.input.youtubeservice import YoutubeService
from pipeline.steps.prediction.videoprediction import VideoPrediction
from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotraining import VideoTrainer

if __name__ == "__main__":
    # model = tf.keras.models.load_model("custommodel42000NG9train.h5")
    # steps = [GoogleDriveService(), VideoPreProcessor(), MPEmbedder(), VideoTrainer(), VideoPrediction(),
    #          VideoEvaluation()]
    # pipeline = Pipeline(
    #     steps=steps, model=None, trainmode=False)  # testdata=False
    # pipeline.process()


    for video in os.listdir(os.sep.join(["data", "production"])):
        MPEmbedder().process([video])


    # create data/production if directory doesn't exist
    if not os.path.exists(os.sep.join(["data", "production"])):
        os.makedirs(os.sep.join(["data", "production"]))

