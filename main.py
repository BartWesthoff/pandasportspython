import numpy as np

from pipeline.steps.embedder.MPEmbedder import MPEmbedder
from pipeline.steps.evaluation.videoevaluation import VideoEvaluation
from pipeline.steps.input.googledriveservice import GoogleDriveService
from pipeline.pipeline import Pipeline
from pipeline.steps.prediction.videoprediction import VideoPrediction
# from pipeline.steps.preprocessors.videopreprocessor import VideoPreProcessor
from pipeline.steps.training.videotraining import VideoTrainer
from pipeline.utils.utils import Utils

if __name__ == "__main__":
    # pipeline = Pipeline(GoogleDriveService(),  MPEmbedder(), VideoTrainer(), VideoPrediction(), VideoEvaluation())
    # pipeline.process()

    squat = Utils.openEmbedding("bart_squat_52")
    print(squat.shape)
    squat = Utils.openEmbedding("bart_squat_51")
    print(squat.shape)



